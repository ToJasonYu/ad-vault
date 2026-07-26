class SessionsController < ApplicationController
  def create
    advertiser = Advertiser.find_by(email: params[:email])

    if advertiser&.authenticate(params[:password])
      render json: { advertiser: serialize(advertiser), token: advertiser.api_token }
    else
      render json: { error: "invalid email or password" }, status: :unauthorized
    end
  end

  private

  def serialize(advertiser)
    { id: advertiser.id, name: advertiser.name, email: advertiser.email }
  end
end
