class Advertiser < ApplicationRecord
  has_secure_password

  validates :name, presence: true
  validates :email, presence: true, uniqueness: true

  before_create :generate_api_token

  private

  def generate_api_token
    self.api_token = SecureRandom.hex(24)
  end
end
