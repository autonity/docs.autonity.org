DOCSY_RELEASE := v0.3.0
.DEFAULT_GOAL := serve

# Install required submodules and npm dependencies. You should re-run this
# target whenever the dependencies have changed.
deps:
	git submodule update --init --recursive
	npm ci --silent --no-progress

# Serve the site with Hugo's local webserver and filesystem monitor. The `deps`
# prerequisite is added mainly for convenience.
serve: deps
	hugo serve

# Build and render the site under the `public/` subdirectory.
build:
	hugo --minify --cleanDestinationDir

# Convenience target to upgrade the Docsy git submodule cloned under
# the `themes/docsy` directory.
.ONESHELL:
upgrade:
	cd themes/docsy
	git fetch
	git checkout $(DOCSY_RELEASE)
	cd ../..
	@echo "Remember to check that 'layouts/partials/page-meta-links.html' is" \
	      "kept in sync with any changes to" \
	      "'themes/docsy/layouts/partials/page-meta-links.html'."

.PHONY: deps serve build upgrade
