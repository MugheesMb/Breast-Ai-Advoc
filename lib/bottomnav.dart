import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:pink/screens/profile.dart';
import 'package:pink/screens/dashboard.dart';
import 'package:pink/utilities/Mytheme.dart';
import 'package:pink/screens/chat/chathome.dart';
import 'package:pink/screens/splash_screen.dart';
import 'package:cupertino_icons/cupertino_icons.dart';
// ignore_for_file: prefer_const_literals_to_create_immutables, prefer_const_constructors


class BottomNav extends StatefulWidget {
  const BottomNav({super.key});

  @override
  State<BottomNav> createState() => _BottomNavState();
}

class _BottomNavState extends State<BottomNav> {
  int pgindex = 0;
  void selindex(int index) {
    setState(() {
      pgindex = index;
    });
  }

  final List<Widget> pages = [DashBoard(), ChatHome(), Profile()];
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: CustomTheme.button,
        type: BottomNavigationBarType.fixed,
        iconSize: 30,
        showSelectedLabels: false,
        showUnselectedLabels: false,
        onTap: selindex,
        currentIndex: pgindex,
        items: [
          BottomNavigationBarItem(
            icon: Icon(Icons.home, color: CustomTheme.black),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.chat_bubble, color: CustomTheme.black),
            label: 'Search',
          ),
          BottomNavigationBarItem(
            icon: Icon(
              CupertinoIcons.profile_circled,
              color: CustomTheme.black,
            ),
            label: 'Reels',
          ),
        ],
      ),
      body: pages[pgindex],
    );
  }
}
