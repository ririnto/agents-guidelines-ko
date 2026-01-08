#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for setup-agents.py"""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Import the module - we need to handle the hyphen in the filename
import importlib.util
import sys

spec = importlib.util.spec_from_file_location(
    "setup_agents",
    Path(__file__).parent / "setup-agents.py"
)
setup_agents = importlib.util.module_from_spec(spec)
sys.modules["setup_agents"] = setup_agents
spec.loader.exec_module(setup_agents)


class TestSetupAgents(unittest.TestCase):
    """Test cases for setup-agents.py functions"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_get_dest_base_with_env_var(self):
        """Test get_dest_base with environment variable"""
        tool_config = {
            "base": Path("/default/path"),
            "env": "TEST_ENV_VAR"
        }
        
        with patch.dict('os.environ', {'TEST_ENV_VAR': '/custom/path'}):
            result = setup_agents.get_dest_base(tool_config)
            self.assertEqual(result, Path('/custom/path'))

    def test_get_dest_base_without_env_var(self):
        """Test get_dest_base without environment variable"""
        tool_config = {
            "base": Path("/default/path")
        }
        
        result = setup_agents.get_dest_base(tool_config)
        self.assertEqual(result, Path('/default/path'))

    def test_backup_and_copy(self):
        """Test backup_and_copy function"""
        # Create source and destination directories
        src_dir = self.temp_path / "source"
        dest_dir = self.temp_path / "destination"
        backup_dir = self.temp_path / "backup"
        
        src_dir.mkdir()
        dest_dir.mkdir()
        
        # Create source file
        source_file = src_dir / "test.md"
        source_file.write_text("Test content")
        
        # Create destination file that will be backed up
        dest_file = dest_dir / "test.md"
        dest_file.write_text("Old content")
        
        # Create logger
        logger = MagicMock()
        
        # Call backup_and_copy
        setup_agents.backup_and_copy(dest_file, backup_dir, source_file, logger)
        
        # Verify file was copied
        self.assertTrue(dest_file.exists())
        self.assertEqual(dest_file.read_text(), "Test content")
        
        # Verify backup was created
        self.assertTrue(backup_dir.exists())
        backup_files = list(backup_dir.iterdir())
        self.assertEqual(len(backup_files), 1)
        self.assertIn("test.", backup_files[0].name)
        self.assertEqual(backup_files[0].read_text(), "Old content")

    def test_backup_naming_with_extension(self):
        """Test backup naming preserves file extension"""
        src_dir = self.temp_path / "source"
        dest_dir = self.temp_path / "destination"
        backup_dir = self.temp_path / "backup"
        
        src_dir.mkdir()
        dest_dir.mkdir()
        
        # Test with .md extension
        source_file = src_dir / "test.md"
        source_file.write_text("Content")
        
        dest_file = dest_dir / "test.md"
        dest_file.write_text("Old")
        
        logger = MagicMock()
        setup_agents.backup_and_copy(dest_file, backup_dir, source_file, logger)
        
        backup_files = list(backup_dir.iterdir())
        self.assertTrue(backup_files[0].name.endswith(".md"))

    def test_backup_naming_without_extension(self):
        """Test backup naming for files without extension"""
        src_dir = self.temp_path / "source"
        dest_dir = self.temp_path / "destination"
        backup_dir = self.temp_path / "backup"
        
        src_dir.mkdir()
        dest_dir.mkdir()
        
        # Test without extension
        source_file = src_dir / "config"
        source_file.write_text("Content")
        
        dest_file = dest_dir / "config"
        dest_file.write_text("Old")
        
        logger = MagicMock()
        setup_agents.backup_and_copy(dest_file, backup_dir, source_file, logger)
        
        backup_files = list(backup_dir.iterdir())
        self.assertTrue(backup_files[0].name.startswith("config."))

    def test_copy_assets_files(self):
        """Test copy_assets with files"""
        src_dir = self.temp_path / "source"
        dest_dir = self.temp_path / "destination"
        
        src_dir.mkdir()
        dest_dir.mkdir()
        
        # Create test files
        (src_dir / "test1.md").write_text("Content 1")
        (src_dir / "test2.md").write_text("Content 2")
        (src_dir / "ignore.txt").write_text("Ignored")  # Non-.md file
        
        logger = MagicMock()
        
        # Mock get_dest_paths to return our test destination
        with patch.object(setup_agents, 'get_dest_paths', return_value=[dest_dir]):
            setup_agents.copy_assets(src_dir, "prompts", False, logger, {"test"})
        
        # Verify only .md files were copied
        self.assertTrue((dest_dir / "test1.md").exists())
        self.assertTrue((dest_dir / "test2.md").exists())
        self.assertFalse((dest_dir / "ignore.txt").exists())

    def test_copy_assets_directories(self):
        """Test copy_assets with directories (skills)"""
        src_dir = self.temp_path / "source"
        dest_dir = self.temp_path / "destination"
        
        src_dir.mkdir()
        dest_dir.mkdir()
        
        # Create test skill directory
        skill_dir = src_dir / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("Skill content")
        (skill_dir / "helper.py").write_text("Helper code")
        
        logger = MagicMock()
        
        # Mock get_dest_paths to return our test destination
        with patch.object(setup_agents, 'get_dest_paths', return_value=[dest_dir]):
            setup_agents.copy_assets(src_dir, "skills", True, logger, {"test"})
        
        # Verify directory was copied with all contents
        self.assertTrue((dest_dir / "test-skill").is_dir())
        self.assertTrue((dest_dir / "test-skill" / "SKILL.md").exists())
        self.assertTrue((dest_dir / "test-skill" / "helper.py").exists())

    def test_cleanup_old_symlinks(self):
        """Test cleanup_old_symlinks removes symlinks"""
        dest_dir = self.temp_path / "destination"
        dest_dir.mkdir()
        
        # Create a regular file
        regular_file = dest_dir / "regular.md"
        regular_file.write_text("Content")
        
        # Create a symlink
        symlink_file = dest_dir / "symlink.md"
        target = self.temp_path / "target.md"
        target.write_text("Target")
        symlink_file.symlink_to(target)
        
        logger = MagicMock()
        
        # Mock CONFIG to point to our test directory
        with patch.dict(setup_agents.CONFIG['destinations'], {
            'test': {
                'base': dest_dir.parent,
                'agents': dest_dir.name,
                'skills': None,
                'prompts': None
            }
        }):
            setup_agents.cleanup_old_symlinks(logger, {"test"})
        
        # Verify symlink was removed but regular file remains
        self.assertTrue(regular_file.exists())
        self.assertFalse(symlink_file.exists())

    def test_load_settings_valid_json(self):
        """Test load_settings with valid JSON"""
        settings_file = self.temp_path / "settings.json"
        settings_data = {"key": "value", "number": 42}
        settings_file.write_text(json.dumps(settings_data))
        
        result = setup_agents.load_settings(settings_file)
        self.assertEqual(result, settings_data)

    def test_load_settings_invalid_json(self):
        """Test load_settings with invalid JSON"""
        settings_file = self.temp_path / "settings.json"
        settings_file.write_text("{ invalid json }")
        
        result = setup_agents.load_settings(settings_file)
        self.assertIsNone(result)

    def test_load_settings_missing_file(self):
        """Test load_settings with missing file"""
        settings_file = self.temp_path / "nonexistent.json"
        
        result = setup_agents.load_settings(settings_file)
        self.assertIsNone(result)

    def test_write_settings(self):
        """Test write_settings creates valid JSON file"""
        settings_dir = self.temp_path / "settings"
        settings_dir.mkdir()
        settings_file = settings_dir / "settings.json"
        
        data = {"key": "value", "nested": {"a": 1, "b": 2}}
        logger = MagicMock()
        
        setup_agents.write_settings(settings_file, settings_dir, data, logger)
        
        # Verify file exists and contains correct data
        self.assertTrue(settings_file.exists())
        loaded_data = json.loads(settings_file.read_text())
        self.assertEqual(loaded_data, data)


if __name__ == '__main__':
    unittest.main()
