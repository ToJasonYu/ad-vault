import { useState } from "react"
import type { NewCampaign } from "../api"

const CATEGORIES = ["sports", "tech", "travel", "finance", "gaming"]

interface CampaignFormProps {
  onCreate: (campaign: NewCampaign) => Promise<void>
}

export default function CampaignForm({ onCreate }: CampaignFormProps) {
  const [name, setName] = useState("")
  const [category, setCategory] = useState(CATEGORIES[0])
  const [budget, setBudget] = useState("")
  const [bidAmount, setBidAmount] = useState("")
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError(null)

    try {
      await onCreate({ name, category, budget: Number(budget), bid_amount: Number(bidAmount) })
      setName("")
      setBudget("")
      setBidAmount("")
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err))
    }
  }

  return (
    <form onSubmit={handleSubmit} className="campaign-form">
      <h3>New campaign</h3>

      <label>
        Name
        <input value={name} onChange={(e) => setName(e.target.value)} required />
      </label>

      <label>
        Category
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </label>

      <label>
        Budget ($)
        <input type="number" min="0" step="0.01" value={budget} onChange={(e) => setBudget(e.target.value)} required />
      </label>

      <label>
        Bid amount ($)
        <input type="number" min="0" step="0.01" value={bidAmount} onChange={(e) => setBidAmount(e.target.value)} required />
      </label>

      {error && <p className="error">{error}</p>}

      <button type="submit">Create campaign</button>
    </form>
  )
}
