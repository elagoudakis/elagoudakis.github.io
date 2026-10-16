# frozen_string_literal: true

source "https://rubygems.org"

gem "jekyll", "~> 4.3"

group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.17"
  gem "jekyll-seo-tag", "~> 2.8"
  gem "jekyll-sitemap", "~> 1.4"
end

group :test do
  gem "html-proofer", "~> 5.0"
end

# Needed for `jekyll serve` on Ruby 3+
gem "webrick", "~> 1.8"

# Time zone data on Windows
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end
