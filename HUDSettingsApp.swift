import SwiftUI

struct ContentView: View {
    @State private var features = [
        Feature(name: "Rear Traffic Alert", isEnabled: false),
        Feature(name: "Headlight Status", isEnabled: false),
        Feature(name: "Turn Signals", isEnabled: false),
        Feature(name: "Navigation", isEnabled: false),
        Feature(name: "Speed Limits", isEnabled: false),
        Feature(name: "Takeover Alerts", isEnabled: false),
        Feature(name: "Lane Departure", isEnabled: false),
        Feature(name: "Autopilot Status", isEnabled: false),
        Feature(name: "Gear Position", isEnabled: false),
        Feature(name: "Battery Range", isEnabled: false),
        Feature(name: "Speed Display", isEnabled: false)
    ]
    
    @State private var selectedTheme = "Dark"
    @State private var statusMessage = "Ready"
    @State private var isSyncing = false
    
    let themes = ["Dark", "Light", "Nature", "Cyber"]
    
    var body: some View {
        NavigationView {
            ZStack {
                Color.black.ignoresSafeArea()
                
                ScrollView {
                    VStack(spacing: 20) {
                        // Dynamic Island Simulation
                        DynamicIslandView()
                        
                        // Header
                        HStack {
                            Text("Settings")
                                .font(.largeTitle.bold())
                                .foregroundColor(.white)
                            Spacer()
                        }
                        .padding(.horizontal)
                        
                        // Status Section
                        VStack(spacing: 0) {
                            SettingRow(
                                title: "Your Drive is up to date",
                                subtitle: "1.1.22",
                                showToggle: false
                            )
                        }
                        .background(Color(red: 0.11, green: 0.11, blue: 0.12))
                        .cornerRadius(16)
                        .padding(.horizontal)
                        
                        // Features Section
                        VStack(spacing: 1) {
                            ForEach(features.indices, id: \.self) { index in
                                SettingRow(
                                    title: features[index].name,
                                    isOn: $features[index].isEnabled,
                                    showToggle: true
                                )
                                .onTapGesture {
                                    features[index].isEnabled.toggle()
                                    updateStatus(for: features[index].name, enabled: features[index].isEnabled)
                                }
                            }
                            
                            Divider()
                                .background(Color.gray)
                                .padding(.horizontal)
                            
                            SettingRow(title: "Navigation settings", showToggle: false, showArrow: true)
                            SettingRow(title: "Units", showToggle: false, showArrow: true)
                        }
                        .background(Color(red: 0.11, green: 0.11, blue: 0.12))
                        .cornerRadius(16)
                        .padding(.horizontal)
                        
                        // Theme Section
                        VStack(alignment: .leading, spacing: 15) {
                            HStack {
                                Text("Theme")
                                    .font(.title2.bold())
                                    .foregroundColor(.white)
                                Spacer()
                            }
                            
                            LazyVGrid(columns: [
                                GridItem(.flexible()),
                                GridItem(.flexible())
                            ], spacing: 10) {
                                ForEach(themes, id: \.self) { theme in
                                    ThemeButton(
                                        title: theme,
                                        isSelected: selectedTheme == theme
                                    ) {
                                        selectedTheme = theme
                                        statusMessage = "Theme set to \(theme) for target device"
                                    }
                                }
                            }
                        }
                        .padding()
                        .background(Color(red: 0.11, green: 0.11, blue: 0.12))
                        .cornerRadius(16)
                        .padding(.horizontal)
                        
                        // Sync Button
                        VStack(spacing: 15) {
                            Button(action: syncSettings) {
                                HStack {
                                    if isSyncing {
                                        ProgressView()
                                            .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                            .scaleEffect(0.8)
                                    }
                                    Text(isSyncing ? "Syncing..." : "Sync Settings")
                                        .font(.headline.bold())
                                        .foregroundColor(.white)
                                }
                                .frame(maxWidth: .infinity)
                                .frame(height: 52)
                                .background(Color.blue)
                                .cornerRadius(14)
                            }
                            .disabled(isSyncing)
                            
                            Text(statusMessage)
                                .font(.footnote.bold())
                                .foregroundColor(Color(red: 0.56, green: 0.56, blue: 0.58))
                        }
                        .padding(.horizontal)
                        
                        Spacer(minLength: 100)
                    }
                }
            }
        }
        .preferredColorScheme(.dark)
    }
    
    private func updateStatus(for feature: String, enabled: Bool) {
        let status = enabled ? "enabled" : "disabled"
        statusMessage = "\(feature) \(status) (pending sync)"
    }
    
    private func syncSettings() {
        isSyncing = true
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
            isSyncing = false
            let enabledCount = features.filter { $0.isEnabled }.count
            statusMessage = enabledCount > 0 ? 
                "Synced to device - \(enabledCount) features enabled" :
                "Synced to device - All features disabled"
        }
    }
}

struct SettingRow: View {
    let title: String
    let subtitle: String?
    @Binding var isOn: Bool
    let showToggle: Bool
    let showArrow: Bool
    
    init(title: String, subtitle: String? = nil, isOn: Binding<Bool> = .constant(false), showToggle: Bool = false, showArrow: Bool = false) {
        self.title = title
        self.subtitle = subtitle
        self._isOn = isOn
        self.showToggle = showToggle
        self.showArrow = showArrow
    }
    
    var body: some View {
        HStack {
            Text(title)
                .font(.body.bold())
                .foregroundColor(.white)
            
            Spacer()
            
            if let subtitle = subtitle {
                Text(subtitle)
                    .font(.body.bold())
                    .foregroundColor(Color(red: 0.56, green: 0.56, blue: 0.58))
            }
            
            if showToggle {
                Toggle("", isOn: $isOn)
                    .toggleStyle(SwitchToggleStyle(tint: Color.green))
            }
            
            if showArrow {
                Image(systemName: "chevron.right")
                    .foregroundColor(Color(red: 0.56, green: 0.56, blue: 0.58))
                    .font(.body.bold())
            }
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 14)
        .contentShape(Rectangle())
    }
}

struct ThemeButton: View {
    let title: String
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.body.bold())
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .frame(height: 38)
                .background(isSelected ? themeColor : Color(red: 0.22, green: 0.22, blue: 0.24))
                .cornerRadius(10)
        }
    }
    
    private var themeColor: Color {
        switch title {
        case "Dark": return .blue
        case "Light": return .blue
        case "Nature": return .green
        case "Cyber": return .pink
        default: return .blue
        }
    }
}

struct DynamicIslandView: View {
    @State private var isExpanded = false
    
    var body: some View {
        Button(action: { isExpanded.toggle() }) {
            HStack {
                if isExpanded {
                    Text("HUD Control Active")
                        .font(.caption.bold())
                        .foregroundColor(.white)
                } else {
                    Circle()
                        .fill(Color.green)
                        .frame(width: 6, height: 6)
                }
            }
            .frame(width: isExpanded ? 200 : 120, height: isExpanded ? 40 : 32)
            .background(Color(red: 0.11, green: 0.11, blue: 0.12))
            .cornerRadius(isExpanded ? 20 : 16)
            .animation(.easeInOut(duration: 0.3), value: isExpanded)
        }
        .padding(.top, 10)
    }
}

struct Feature {
    let name: String
    var isEnabled: Bool
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

@main
struct HUDSettingsApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}