import { useEffect, useState } from "react"
import AuthForm from "./components/AuthForm"
import CampaignForm from "./components/CampaignForm"
import CampaignList from "./components/CampaignList"
import { createCampaign, listCampaigns } from "./api"
import "./App.css"

function App() {
  const [token, setToken] = useState(() => localStorage.getItem("token"))
  const [advertiser, setAdvertiser] = useState(() => {
    const stored = localStorage.getItem("advertiser")
    return stored ? JSON.parse(stored) : null
  })
  const [campaigns, setCampaigns] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!token) return

    listCampaigns(token)
      .then(setCampaigns)
      .catch((err) => setError(err.message))
  }, [token])

  function handleAuthenticated(newAdvertiser, newToken) {
    localStorage.setItem("token", newToken)
    localStorage.setItem("advertiser", JSON.stringify(newAdvertiser))
    setToken(newToken)
    setAdvertiser(newAdvertiser)
  }

  function handleLogout() {
    localStorage.removeItem("token")
    localStorage.removeItem("advertiser")
    setToken(null)
    setAdvertiser(null)
    setCampaigns([])
  }

  async function handleCreateCampaign(campaign) {
    const created = await createCampaign(token, campaign)
    setCampaigns((prev) => [...prev, created])
  }

  if (!token) {
    return (
      <div className="app">
        <h1>ad-vault</h1>
        <AuthForm onAuthenticated={handleAuthenticated} />
      </div>
    )
  }

  return (
    <div className="app">
      <header>
        <h1>ad-vault</h1>
        <div>
          <span>{advertiser?.name}</span>
          <button onClick={handleLogout}>Log out</button>
        </div>
      </header>

      {error && <p className="error">{error}</p>}

      <CampaignList campaigns={campaigns} />
      <CampaignForm onCreate={handleCreateCampaign} />
    </div>
  )
}

export default App
