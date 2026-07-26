class Campaign < ApplicationRecord
  belongs_to :advertiser
  has_many :events, dependent: :destroy

  validates :name, presence: true
  validates :category, presence: true
  validates :budget, numericality: { greater_than: 0 }
  validates :bid_amount, numericality: { greater_than: 0 }
end
