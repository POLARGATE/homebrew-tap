cask "polarbat" do
  version "0.2.2,659"
  sha256 "f71205037d32ed6951cfd01ac40126456d8eba9770c3500010d202d6ef749f72"

  url "https://gysinhqxvelxxudbchez.supabase.co/storage/v1/object/public/downloads/polarbat/PolarBat-#{version.csv.first}-#{version.csv.second}.dmg",
      verified: "gysinhqxvelxxudbchez.supabase.co/storage/v1/object/public/downloads/polarbat/"
  name "PolarBat"
  desc "Menu bar app to keep the computer awake, lid closed included"
  homepage "https://polarbat.com/en"

  livecheck do
    url "https://polargate.ai/polarbat/appcast.xml"
    strategy :sparkle
  end

  auto_updates true
  depends_on arch: :arm64
  depends_on macos: :tahoe

  app "PolarBat.app"

  uninstall launchctl: "ai.polargate.polarbat.backstop",
            quit:      "ai.polargate.polarbat"

  zap trash: [
    "~/Library/Application Support/PolarBat",
    "~/Library/Caches/ai.polargate.polarbat",
    "~/Library/HTTPStorages/ai.polargate.polarbat",
    "~/Library/LaunchAgents/ai.polargate.polarbat.backstop.plist",
    "~/Library/Preferences/ai.polargate.polarbat.plist",
  ]
end
