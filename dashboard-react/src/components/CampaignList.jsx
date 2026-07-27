export default function CampaignList({ campaigns }) {
  if (campaigns.length === 0) {
    return <p>No campaigns yet — create one below.</p>
  }

  return (
    <table className="campaign-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Category</th>
          <th>Budget</th>
          <th>Remaining</th>
          <th>Impressions</th>
          <th>Clicks</th>
          <th>Spend</th>
        </tr>
      </thead>
      <tbody>
        {campaigns.map((campaign) => (
          <tr key={campaign.id}>
            <td>{campaign.name}</td>
            <td>{campaign.category}</td>
            <td>${Number(campaign.budget).toFixed(2)}</td>
            <td>${Number(campaign.budget_remaining).toFixed(2)}</td>
            <td>{campaign.impressions}</td>
            <td>{campaign.clicks}</td>
            <td>${Number(campaign.spend).toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
