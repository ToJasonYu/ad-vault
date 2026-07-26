class CreateAdvertisers < ActiveRecord::Migration[8.1]
  def change
    create_table :advertisers do |t|
      t.string :name, null: false
      t.string :email, null: false
      t.string :password_digest, null: false
      t.string :api_token, null: false

      t.timestamps
    end
    add_index :advertisers, :email, unique: true
    add_index :advertisers, :api_token, unique: true
  end
end
