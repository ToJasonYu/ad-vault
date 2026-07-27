# Be sure to restart your server when you modify this file.

# The React dashboard runs on a different origin (port) than this API in
# development, so the browser needs an explicit CORS allowance to call it.

Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins "http://localhost:5173", "http://127.0.0.1:5173"

    resource "*",
      headers: :any,
      methods: [:get, :post, :put, :patch, :delete, :options, :head]
  end
end
