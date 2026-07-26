# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[8.1].define(version: 2026_07_26_081921) do
  create_table "advertisers", force: :cascade do |t|
    t.string "api_token", null: false
    t.datetime "created_at", null: false
    t.string "email", null: false
    t.string "name", null: false
    t.string "password_digest", null: false
    t.datetime "updated_at", null: false
    t.index ["api_token"], name: "index_advertisers_on_api_token", unique: true
    t.index ["email"], name: "index_advertisers_on_email", unique: true
  end

  create_table "campaigns", force: :cascade do |t|
    t.integer "advertiser_id", null: false
    t.decimal "bid_amount", precision: 10, scale: 2, null: false
    t.decimal "budget", precision: 10, scale: 2, null: false
    t.decimal "budget_remaining", precision: 10, scale: 2, null: false
    t.string "category", null: false
    t.datetime "created_at", null: false
    t.string "name", null: false
    t.datetime "updated_at", null: false
    t.index ["advertiser_id"], name: "index_campaigns_on_advertiser_id"
  end

  add_foreign_key "campaigns", "advertisers"
end
