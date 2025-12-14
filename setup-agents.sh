#!/usr/bin/env sh

# ==========================================
# [안전 모드 설정]
# set -e (제거됨): 실패해도 계속 진행하기 위해 제거
# set -u: 정의되지 않은 변수 사용 시 오류
# ==========================================
set -euo pipefail

# ==========================================
# [설정 변수]
# ==========================================
BASE_DIR="$HOME/.agents-guidelines"
MAIN_INSTRUCTION_FILE="copilot-instructions.md"
MAIN_PATH="$BASE_DIR/$MAIN_INSTRUCTION_FILE"

# 경로 변수
VSCODE_SETTINGS_FILE="$HOME/Library/Application Support/Code/User/settings.json"
INTELLIJ_CONFIG_DIR="$HOME/.config/github-copilot/intellij"
INTELLIJ_TARGET_FILENAME="global-copilot-instructions.md"
CLAUDE_LINK="$HOME/CLAUDE.md"

# 쉘 설정 파일 감지
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
else
    SHELL_RC="$HOME/.profile"
fi

# 실행 플래그 (0: False, 1: True)
DO_VSCODE=0
DO_INTELLIJ=0
DO_CLAUDE=0
DO_CODEX=0

# 결과 상태 저장 변수 (기본값: 건너뜀)
RES_VSCODE="⛔ Skipped"
RES_INTELLIJ="⛔ Skipped"
RES_CLAUDE="⛔ Skipped"
RES_CODEX="⛔ Skipped"

# ==========================================
# [유틸리티 함수]
# ==========================================
log_info() { printf "\033[1;32m[INFO]\033[0m %s\n" "$1"; }
log_warn() { printf "\033[1;33m[WARN]\033[0m %s\n" "$1"; }
log_error() { printf "\033[1;31m[ERROR]\033[0m %s\n" "$1"; }

show_help() {
    echo "사용법: $0 [옵션]"
    echo ""
    echo "옵션:"
    echo "  --all       모든 도구 설정"
    echo "  --vscode    VS Code (GitHub Copilot) 설정"
    echo "  --intellij  IntelliJ (GitHub Copilot) 설정"
    echo "  --claude    Claude Code (CLAUDE.md) 설정"
    echo "  --codex     Codex 및 쉘 환경 변수 설정"
    echo "  --help      도움말 표시"
}

# ==========================================
# [1. 인자 파싱]
# ==========================================
if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

while [ $# -gt 0 ]; do
    case "$1" in
        --all)
        DO_VSCODE=1; DO_INTELLIJ=1; DO_CLAUDE=1; DO_CODEX=1 ;;
        --vscode)   DO_VSCODE=1 ;;
        --intellij) DO_INTELLIJ=1 ;;
        --claude)   DO_CLAUDE=1 ;;
        --codex)    DO_CODEX=1 ;;
        --help|-h)  show_help; exit 0 ;;
        *)          log_error "알 수 없는 옵션: $1"; show_help; exit 1 ;;
    esac
    shift
done

# ==========================================
# [2. 공통 사전 점검 (필수)]
# ==========================================
log_info "환경 점검 중..."

if [ ! -d "$BASE_DIR" ]; then
    log_error "디렉터리를 찾을 수 없습니다: $BASE_DIR"
    echo "❌ 필수 경로가 없어 스크립트를 중단합니다."
    exit 1
fi

if [ ! -f "$MAIN_PATH" ]; then
    log_error "메인 지침 파일을 찾을 수 없습니다: $MAIN_PATH"
    echo "❌ 필수 파일이 없어 스크립트를 중단합니다."
    exit 1
fi

# ==========================================
# [3. VS Code 설정]
# ==========================================
if [ "$DO_VSCODE" -eq 1 ]; then
    log_info "VS Code (Copilot) 설정 적용 중..."
    
    # 서브쉘(()를 이용해 오류가 발생해도 메인 스크립트 변수에 영향 주지 않도록 하거나
    # if 문으로 흐름 제어
    if ! command -v jq >/dev/null 2>&1; then
        log_error "'jq'가 설치되어 있지 않습니다."
        RES_VSCODE="❌ Failed (jq missing)"
        elif [ ! -f "$VSCODE_SETTINGS_FILE" ]; then
        log_warn "VS Code 설정 파일을 찾을 수 없습니다."
        RES_VSCODE="❌ Failed (File not found)"
    else
        TMP_FILE=$(mktemp)
        # jq 실행 시도
        if jq --arg key "chat.instructionsFilesLocations" \
        --arg path "$BASE_DIR" \
        '.[$key] = (.[$key] // {}) + {($path): true}' \
        "$VSCODE_SETTINGS_FILE" > "$TMP_FILE"; then
            
            if [ -s "$TMP_FILE" ]; then
                mv "$TMP_FILE" "$VSCODE_SETTINGS_FILE"
                log_info "✅ VS Code settings.json 업데이트 완료."
                RES_VSCODE="✅ Success"
            else
                log_error "jq 결과 파일이 비어 있습니다."
                RES_VSCODE="❌ Failed (Empty JSON)"
            fi
        else
            log_error "jq 실행 중 오류 발생."
            RES_VSCODE="❌ Failed (jq error)"
        fi
        # 임시 파일 정리
        [ -f "$TMP_FILE" ] && rm "$TMP_FILE"
    fi
fi

# ==========================================
# [4. IntelliJ Copilot 설정]
# ==========================================
if [ "$DO_INTELLIJ" -eq 1 ]; then
    log_info "IntelliJ (GitHub Copilot) 설정 적용 중..."
    
    # 디렉터리 생성 시도
    if ! mkdir -p "$INTELLIJ_CONFIG_DIR" 2>/dev/null; then
        log_error "디렉터리 생성 실패: $INTELLIJ_CONFIG_DIR"
        RES_INTELLIJ="❌ Failed (Mkdir error)"
    else
        INTELLIJ_LINK="$INTELLIJ_CONFIG_DIR/$INTELLIJ_TARGET_FILENAME"
        
        # 기존 파일 백업
        if [ -f "$INTELLIJ_LINK" ] && [ ! -L "$INTELLIJ_LINK" ]; then
            mv "$INTELLIJ_LINK" "${INTELLIJ_LINK}.bak"
            log_warn "기존 파일 백업됨."
        fi
        
        # 링크 생성 시도
        if ln -sf "$MAIN_PATH" "$INTELLIJ_LINK"; then
            log_info "✅ IntelliJ 설정 연결 완료."
            RES_INTELLIJ="✅ Success"
        else
            log_error "심볼릭 링크 생성 실패."
            RES_INTELLIJ="❌ Failed (Link error)"
        fi
    fi
fi

# ==========================================
# [5. Claude Code 설정]
# ==========================================
if [ "$DO_CLAUDE" -eq 1 ]; then
    log_info "Claude Code 설정 적용 중..."
    
    # 기존 파일 백업
    if [ -f "$CLAUDE_LINK" ] && [ ! -L "$CLAUDE_LINK" ]; then
        mv "$CLAUDE_LINK" "${CLAUDE_LINK}.bak"
        log_warn "기존 CLAUDE.md 백업됨."
    fi
    
    if ln -sf "$MAIN_PATH" "$CLAUDE_LINK"; then
        log_info "✅ ~/CLAUDE.md 심볼릭 링크 연결 완료."
        RES_CLAUDE="✅ Success"
    else
        log_error "심볼릭 링크 생성 실패."
        RES_CLAUDE="❌ Failed (Link error)"
    fi
fi

# ==========================================
# [6. Codex / CLI Tools 설정]
# ==========================================
if [ "$DO_CODEX" -eq 1 ]; then
    log_info "Codex 및 CLI 도구 설정 적용 중..."
    
    ENV_VAR_NAME="AI_AGENTS_RULES_PATH"
    EXPORT_CMD="export $ENV_VAR_NAME=\"$MAIN_PATH\""
    ALIAS_CMD="alias codex='codex --system-prompt-file \"\$$ENV_VAR_NAME\"'"
    
    if grep -q "$ENV_VAR_NAME" "$SHELL_RC" 2>/dev/null; then
        log_info "이미 설정이 존재합니다."
        RES_CODEX="✅ Success (Already exists)"
    else
        # 파일 쓰기 시도
        if {
            echo ""
            echo "# --- AI Agents Guidelines Setup ---"
            echo "$EXPORT_CMD"
            echo "$ALIAS_CMD"
            echo "# ----------------------------------"
            } >> "$SHELL_RC"; then
            log_info "✅ 쉘 설정 추가 완료."
            RES_CODEX="✅ Success"
        else
            log_error "쉘 설정 파일 쓰기 실패: $SHELL_RC"
            RES_CODEX="❌ Failed (Write error)"
        fi
    fi
fi

# ==========================================
# [최종 요약 리포트]
# ==========================================
echo ""
echo "=========================================="
echo "         설정 결과 요약 (Summary)          "
echo "=========================================="
echo " 1. VS Code   : $RES_VSCODE"
echo " 2. IntelliJ  : $RES_INTELLIJ"
echo " 3. Claude    : $RES_CLAUDE"
echo " 4. Codex     : $RES_CODEX"
echo "=========================================="
echo ""

# Codex 성공 시 안내 메시지
case "$RES_CODEX" in
    *"Success"*)
        echo "💡 Codex 설정을 적용하려면 다음 명령어를 실행하세요:"
        echo "   source $SHELL_RC"
    ;;
esac
