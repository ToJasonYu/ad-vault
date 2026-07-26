class CreateEvents < ActiveRecord::Migration[8.1]
  def change
    create_table :events do |t|
      t.references :campaign, null: false, foreign_key: true
      t.string :event_type, null: false

      t.timestamps
    end
  end
end
