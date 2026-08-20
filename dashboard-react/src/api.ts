export interface Advertiser {
  id: number
  name: string
  email: string
}

export interface Campaign {
  id: number
  name: string
  category: string
  budget: number
  bid_amount: number
  budget_remaining: number
  impressions: number
  clicks: number
  spend: number
}

export interface NewCampaign {
  name: string
  category: string
  budget: number
  bid_amount: number
}

interface AuthResponse {
  advertiser: Advertiser
  token: string
}

interface RequestOptions {
  method?: string
  token?: string
  body?: unknown
}

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:3000"

async function request<T>(path: string, { method = "GET", token, body }: RequestOptions = {}): Promise<T> {
  const headers: Record<string, string> = { "Content-Type": "application/json" }
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

export function signup(name: string, email: string, password: string) {
  return request<AuthResponse>("/signup", { method: "POST", body: { name, email, password } })
}

export function login(email: string, password: string) {
  return request<AuthResponse>("/login", { method: "POST", body: { email, password } })
}

export function listCampaigns(token: string) {
  return request<Campaign[]>("/campaigns", { token })
}

export function createCampaign(token: string, campaign: NewCampaign) {
  return request<Campaign>("/campaigns", { method: "POST", token, body: campaign })
}
