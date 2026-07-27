class CampaignsController < ApplicationController
  before_action :set_campaign, only: [:show, :update]

  def index
    render json: @current_advertiser.campaigns.map { |campaign| serialize(campaign) }
  end

  def show
    render json: serialize(@campaign)
  end

  def create
    campaign = @current_advertiser.campaigns.new(campaign_params)
    campaign.budget_remaining = campaign.budget

    if campaign.save
      render json: serialize(campaign), status: :created
    else
      render json: { errors: campaign.errors.full_messages }, status: :unprocessable_entity
    end
  end

  def update
    if @campaign.update(campaign_params)
      render json: serialize(@campaign)
    else
      render json: { errors: @campaign.errors.full_messages }, status: :unprocessable_entity
    end
  end

  private

  def set_campaign
    @campaign = @current_advertiser.campaigns.find_by(id: params[:id])
    render json: { error: "not found" }, status: :not_found unless @campaign
  end

  def campaign_params
    params.permit(:name, :category, :budget, :bid_amount)
  end

  def serialize(campaign)
    {
      id: campaign.id,
      name: campaign.name,
      category: campaign.category,
      budget: campaign.budget,
      bid_amount: campaign.bid_amount,
      budget_remaining: campaign.budget_remaining,
      impressions: campaign.events.where(event_type: "impression").count,
      clicks: campaign.events.where(event_type: "click").count,
      spend: campaign.budget.to_f - campaign.budget_remaining.to_f,
    }
  end
end
