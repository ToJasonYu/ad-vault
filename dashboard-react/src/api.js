const BASE_URL = import.meta.env?.VITE_API_BASE_URL || "http://127.0.0.1:3000"

async function request(path, { method = "GET", token, body } = {}) {
  const headers = { "Content-Type": "application/json" }
  if (token) headers.Authorization = `Bearer ${token}`

  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  })

  const data = await response.json()

  if (!response.ok) {
    const message = data.errors ? data.errors.join(", ") : data.error || "request failed"
    throw new Error(message)
  }

  return data
}

export function signup(name, email, password) {
  return request("/signup", { method: "POST", body: { name, email, password } })
}

export function login(email, password) {
  return request("/login", { method: "POST", body: { email, password } })
}

export function listCampaigns(token) {
  return request("/campaigns", { token })
}

export function createCampaign(token, campaign) {
  return request("/campaigns", { method: "POST", token, body: campaign })
}
