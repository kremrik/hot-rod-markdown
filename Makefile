SHELL := bash
MODULE := $(shell cat .package-name)
LINE_LENGTH := 59
NO_COLOR := \e[39m
BLUE := \e[34m
GREEN := \e[32m

#----------------------------------------------------------

.PHONY: check
check : unit-tests type-check black-format flake8-lint code-coverage success

.PHONY: unit-tests
unit-tests :
	@echo
	@echo -e '$(BLUE)unit-tests'
	@echo -e        '----------$(NO_COLOR)'
	@python3 -m pytest tests/unit
	
.PHONY: code-coverage
code-coverage : cov
	@echo
	@echo -e '$(BLUE)code-coverage'
	@echo -e 		'-------------$(NO_COLOR)'
	@coverage-badge -f -o images/coverage.svg

.PHONY: type-check
type-check :
	@echo
	@echo -e '$(BLUE)type-check'
	@echo -e 		'----------$(NO_COLOR)'
	@mypy $(MODULE)
	@mypy cli

.PHONY: black-format
black-format :
	@echo
	@echo -e '$(BLUE)black-format'
	@echo -e 		'------------$(NO_COLOR)'
	@black $(MODULE) -l $(LINE_LENGTH)
	@black cli -l $(LINE_LENGTH)
	@black tests -l $(LINE_LENGTH)

.PHONY: flake8-lint
flake8-lint :
	@echo
	@echo -e '$(BLUE)flake8-lint'
	@echo -e 		'-----------$(NO_COLOR)'
	@flake8 $(MODULE) \
		--max-line-length $(LINE_LENGTH) \
		--ignore=F401,E731,F403 \
		--count \
		|| exit 1

.PHONY: success
success :
	@echo
	@echo -e '$(GREEN)ALL CHECKS COMPLETED SUCCESSFULLY$(NO_COLOR)'

#----------------------------------------------------------

.PHONY: cov
cov:
	@python -m pytest --cov=. --cov-config=.coveragerc --cov-report html

.PHONY: coverage
coverage: cov
	@python3 -m http.server 8000 --directory htmlcov/

.PHONY: set-hooks
set-hooks:
	@git config core.hooksPath .githooks
	@chmod +x .githooks/*
