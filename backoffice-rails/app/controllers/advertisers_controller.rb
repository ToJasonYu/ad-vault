class AdvertisersController < ApplicationController
  def create
    advertiser = Advertiser.new(advertiser_params)

    if advertiser.save
      render json: { advertiser: serialize(advertiser), token: advertiser.api_token }, status: :created
    else
      render json: { errors: advertiser.errors.full_messages }, status: :unprocessable_entity
    end
  end

  private

  def advertiser_params
    params.permit(:name, :email, :password)
  end

  def serialize(advertiser)
    { id: advertiser.id, name: advertiser.name, email: advertiser.email }
  end
end
