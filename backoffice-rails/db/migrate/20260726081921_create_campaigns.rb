class CreateCampaigns < ActiveRecord::Migration[8.1]
  def change
    create_table :campaigns do |t|
      t.references :advertiser, null: false, foreign_key: true
      t.string :name, null: false
      t.string :category, null: false
      t.decimal :budget, precision: 10, scale: 2, null: false
      t.decimal :bid_amount, precision: 10, scale: 2, null: false
      t.decimal :budget_remaining, precision: 10, scale: 2, null: false

      t.timestamps
    end
  end
end
