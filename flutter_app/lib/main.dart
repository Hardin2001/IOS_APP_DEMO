import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';

void main() {
  runApp(HUDSettingsApp());
}

class HUDSettingsApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'HUD Settings',
      theme: ThemeData.dark(),
      home: HUDSettingsPage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class HUDSettingsPage extends StatefulWidget {
  @override
  _HUDSettingsPageState createState() => _HUDSettingsPageState();
}

class _HUDSettingsPageState extends State<HUDSettingsPage> {
  Map<String, bool> features = {
    'Rear Traffic Alert': false,
    'Headlight Status': false,
    'Turn Signals': false,
    'Navigation': false,
    'Speed Limits': false,
    'Takeover Alerts': false,
    'Lane Departure': false,
    'Autopilot Status': false,
    'Gear Position': false,
    'Battery Range': false,
    'Speed Display': false,
  };

  String selectedTheme = 'Dark';
  String statusMessage = 'Ready';
  bool isSyncing = false;

  final List<String> themes = ['Dark', 'Light', 'Nature', 'Cyber'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: CustomScrollView(
          slivers: [
            // Dynamic Island Simulation
            SliverToBoxAdapter(
              child: DynamicIsland(),
            ),
            
            // Header
            SliverToBoxAdapter(
              child: Padding(
                padding: EdgeInsets.all(20),
                child: Text(
                  'Settings',
                  style: TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
              ),
            ),

            // Status Section
            SliverToBoxAdapter(
              child: Container(
                margin: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                padding: EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Color(0xFF1C1C1E),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Your Drive is up to date',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Text(
                          '1.1.22',
                          style: TextStyle(
                            color: Colors.grey,
                            fontSize: 12,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),

            // Features Section
            SliverToBoxAdapter(
              child: Container(
                margin: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                decoration: BoxDecoration(
                  color: Color(0xFF1C1C1E),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  children: [
                    ...features.entries.map((entry) => 
                      FeatureToggle(
                        title: entry.key,
                        value: entry.value,
                        onChanged: (value) {
                          setState(() {
                            features[entry.key] = value;
                            statusMessage = '${entry.key} ${value ? "enabled" : "disabled"} (pending sync)';
                          });
                        },
                      ),
                    ).toList(),
                    Divider(color: Colors.grey.shade800),
                    ListTile(
                      title: Text(
                        'Navigation settings',
                        style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                      ),
                      trailing: Icon(Icons.chevron_right, color: Colors.grey),
                    ),
                    ListTile(
                      title: Text(
                        'Units',
                        style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                      ),
                      trailing: Icon(Icons.chevron_right, color: Colors.grey),
                    ),
                  ],
                ),
              ),
            ),

            // Theme Section
            SliverToBoxAdapter(
              child: Container(
                margin: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                padding: EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Color(0xFF1C1C1E),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Theme',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    SizedBox(height: 15),
                    GridView.count(
                      crossAxisCount: 2,
                      crossAxisSpacing: 10,
                      mainAxisSpacing: 10,
                      childAspectRatio: 3,
                      shrinkWrap: true,
                      physics: NeverScrollableScrollPhysics(),
                      children: themes.map((theme) => 
                        ThemeButton(
                          title: theme,
                          isSelected: selectedTheme == theme,
                          onPressed: () {
                            setState(() {
                              selectedTheme = theme;
                              statusMessage = 'Theme set to $theme for target device';
                            });
                          },
                        ),
                      ).toList(),
                    ),
                  ],
                ),
              ),
            ),

            // Sync Button
            SliverToBoxAdapter(
              child: Padding(
                padding: EdgeInsets.all(20),
                child: Column(
                  children: [
                    ElevatedButton(
                      onPressed: isSyncing ? null : _syncSettings,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.blue,
                        minimumSize: Size(double.infinity, 52),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(14),
                        ),
                      ),
                      child: isSyncing
                          ? Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                SizedBox(
                                  width: 20,
                                  height: 20,
                                  child: CircularProgressIndicator(
                                    strokeWidth: 2,
                                    color: Colors.white,
                                  ),
                                ),
                                SizedBox(width: 10),
                                Text(
                                  'Syncing...',
                                  style: TextStyle(
                                    fontWeight: FontWeight.bold,
                                    color: Colors.white,
                                  ),
                                ),
                              ],
                            )
                          : Text(
                              'Sync Settings',
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                    ),
                    SizedBox(height: 15),
                    Text(
                      statusMessage,
                      style: TextStyle(
                        color: Colors.grey,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _syncSettings() async {
    setState(() {
      isSyncing = true;
    });

    await Future.delayed(Duration(milliseconds: 1500));

    setState(() {
      isSyncing = false;
      int enabledCount = features.values.where((v) => v).length;
      statusMessage = enabledCount > 0
          ? 'Synced to device - $enabledCount features enabled'
          : 'Synced to device - All features disabled';
    });
  }
}

class FeatureToggle extends StatelessWidget {
  final String title;
  final bool value;
  final ValueChanged<bool> onChanged;

  const FeatureToggle({
    Key? key,
    required this.title,
    required this.value,
    required this.onChanged,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(
        title,
        style: TextStyle(
          color: Colors.white,
          fontWeight: FontWeight.bold,
        ),
      ),
      trailing: CupertinoSwitch(
        value: value,
        onChanged: onChanged,
        activeColor: Colors.green,
      ),
    );
  }
}

class ThemeButton extends StatelessWidget {
  final String title;
  final bool isSelected;
  final VoidCallback onPressed;

  const ThemeButton({
    Key? key,
    required this.title,
    required this.isSelected,
    required this.onPressed,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    Color getThemeColor() {
      switch (title) {
        case 'Nature':
          return Colors.green;
        case 'Cyber':
          return Colors.pink;
        default:
          return Colors.blue;
      }
    }

    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: isSelected ? getThemeColor() : Color(0xFF38383A),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10),
        ),
      ),
      child: Text(
        title,
        style: TextStyle(
          color: Colors.white,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}

class DynamicIsland extends StatefulWidget {
  @override
  _DynamicIslandState createState() => _DynamicIslandState();
}

class _DynamicIslandState extends State<DynamicIsland>
    with SingleTickerProviderStateMixin {
  bool isExpanded = false;
  late AnimationController _animationController;
  late Animation<double> _widthAnimation;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: Duration(milliseconds: 300),
      vsync: this,
    );
    _widthAnimation = Tween<double>(begin: 120, end: 200).animate(
      CurvedAnimation(parent: _animationController, curve: Curves.easeInOut),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: GestureDetector(
        onTap: () {
          setState(() {
            isExpanded = !isExpanded;
            if (isExpanded) {
              _animationController.forward();
            } else {
              _animationController.reverse();
            }
          });
        },
        child: AnimatedBuilder(
          animation: _widthAnimation,
          builder: (context, child) {
            return Container(
              width: _widthAnimation.value,
              height: isExpanded ? 40 : 32,
              margin: EdgeInsets.only(top: 10),
              decoration: BoxDecoration(
                color: Color(0xFF1C1C1E),
                borderRadius: BorderRadius.circular(isExpanded ? 20 : 16),
              ),
              child: Center(
                child: isExpanded
                    ? Text(
                        'HUD Control Active',
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 12,
                        ),
                      )
                    : Container(
                        width: 6,
                        height: 6,
                        decoration: BoxDecoration(
                          color: Colors.green,
                          shape: BoxShape.circle,
                        ),
                      ),
              ),
            );
          },
        ),
      ),
    );
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }
}