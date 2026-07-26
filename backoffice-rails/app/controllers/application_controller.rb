class ApplicationController < ActionController::API
  before_action :authenticate_advertiser!

  private

  def authenticate_advertiser!
    token = request.headers["Authorization"]&.split(" ")&.last
    @current_advertiser = Advertiser.find_by(api_token: token)

    render json: { error: "unauthorized" }, status: :unauthorized unless @current_advertiser
  end
end
