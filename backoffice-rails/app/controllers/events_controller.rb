class EventsController < ApplicationController
  skip_before_action :authenticate_advertiser!, only: [:create]

  def create
    campaign = Campaign.find_by(id: params[:campaign_id])
    return render json: { error: "campaign not found" }, status: :not_found unless campaign

    event = campaign.events.new(event_type: params[:event_type])

    if event.save
      decrement_budget(campaign) if event.event_type == "click"
      render json: serialize(event), status: :created
    else
      render json: { errors: event.errors.full_messages }, status: :unprocessable_entity
    end
  end

  private

  # single UPDATE statement so concurrent clicks can't race past each other
  # on a read-modify-write and push the remaining budget below zero
  def decrement_budget(campaign)
    Campaign.where(id: campaign.id).update_all(["budget_remaining = MAX(budget_remaining - ?, 0)", campaign.bid_amount])
  end

  def serialize(event)
    { id: event.id, campaign_id: event.campaign_id, event_type: event.event_type, created_at: event.created_at }
  end
end
