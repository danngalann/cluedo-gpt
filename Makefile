# Define a function to install git hooks
install-hooks:
	@echo "Installing git hooks..."
	@mkdir -p .git/hooks
	@cp -f tooling/githooks/* .git/hooks/ 2>/dev/null || :
	@chmod +x .git/hooks/*
	@echo "Git hooks installed successfully"