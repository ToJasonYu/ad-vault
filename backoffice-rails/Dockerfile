# runs in development mode - production would need RAILS_MASTER_KEY injected
# as a real secret (e.g. a Kubernetes Secret), which is out of scope here
FROM ruby:3.3-slim
WORKDIR /app

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends build-essential libsqlite3-dev sqlite3 && \
    rm -rf /var/lib/apt/lists/*

COPY Gemfile Gemfile.lock ./
RUN bundle install

COPY . .
RUN bundle exec rails db:prepare

EXPOSE 3000
CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0", "-p", "3000"]
