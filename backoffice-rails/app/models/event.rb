class Event < ApplicationRecord
  belongs_to :campaign

  validates :event_type, presence: true, inclusion: { in: %w[impression click] }
end
