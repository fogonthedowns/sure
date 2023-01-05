# Go related commands

## make - show help https://stackoverflow.com/questions/8889035/how-to-document-a-makefile
HELP_FORMAT = \
         %help; \
         while(<>) { push @{$$help{$$2 // 'options'}}, [$$1, $$3] if /^(\w+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/ }; \
         print "usage: make [target]\n\n"; \
     for (keys %help) { \
         print "$$_:\n"; $$sep = " " x (20 - length $$_->[0]); \
         print "  $$_->[0]$$sep$$_->[1]\n" for @{$$help{$$_}}; \
         print "\n"; }

help:   ##@Miscellaneous   Show this help.
	@echo
	@echo "Thank you for reviewing this code"
	@echo
	@echo
	@echo "python3 main.py create '{\"name\": \"Jane Smith\", \"coverage_type\": \"basic\", \"state\": \"CA\", \"has_pet\": false, \"flood_coverage\": true}'"
	@echo 
	@perl -e '$(HELP_FORMAT)' $(MAKEFILE_LIST)

.PHONY: test
test:          ##@Tests   Runs integration test
	python3 -m unittest test_quote.py

.PHONY: setup
setup:         ##@Database Runs inital migratiosn
	python3 main.py setup '{}'
