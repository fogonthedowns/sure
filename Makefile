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
	@echo
	@echo "--------------------------------------------------------------------------------------------------------------"
	@echo "| Thank you for considering me for this opportunity, I am grateful for the opportunity to interview with you |"
	@echo "--------------------------------------------------------------------------------------------------------------"
	@echo
	@echo "    The first thing you'll need to do is ensure you have mysql and all of the dependencies installed. Check out the README."
	@echo "    set the following environment variables: MYSQL_USER, MYSQL_HOST, and MYSQL_PASSWORD. These are read in db.py"
	@echo
	@echo
	@echo
	@echo
	@echo "create Quote:"
	@echo
	@echo "    python3 main.py create '{\"name\": \"Jane Smith\", \"coverage_type\": \"basic\", \"state\": \"CA\", \"has_pet\": false, \"flood_coverage\": true}'"
	@echo
	@echo
	@echo "retreive Quote:"
	@echo
	@echo "    python3 main.py retrieve '{\"uuid\": \"dc4aab71-2d0b-4cf3-938c-caa11f2bc24a\"}'"
	@echo 
	@echo
	@echo "Add State:"
	@echo
	@echo "    python3 main.py create_rate '{\"state\": \"UT\", \"state_tax_percent\": 0.085, \"flood_percent\": 0.001, \"default_rate\":20, \"premium_rate\":40, \"pet_rate\":20}'"
	@echo
	@echo
	@echo "Update State:"
	@echo
	@echo "    python3 main.py update_rate '{\"state\": \"UT\", \"state_tax_percent\": 0.085, \"flood_percent\": 0.001, \"default_rate\":20, \"premium_rate\":40, \"pet_rate\":20}'"
	@echo
	@echo
	@echo "Update State Rates:"
	@echo
	@echo "    python3 main.py retrieve '{\"uuid\": \"dc4aab71-2d0b-4cf3-938c-caa11f2bc24a\"}'"
	@echo 
	@echo

	@perl -e '$(HELP_FORMAT)' $(MAKEFILE_LIST)

.PHONY: test
test:          ##@Tests   Runs integration test
	python3 -m unittest test_quote.py

.PHONY: setup
setup:         ##@Database Runs inital migratiosn
	python3 main.py setup '{}'
