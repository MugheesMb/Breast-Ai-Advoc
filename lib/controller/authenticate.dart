import 'package:flutter/material.dart';
import 'package:pink/screens/dashboard.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:pink/screens/auth/loginPage.dart';

class Authenticate extends StatelessWidget {
  FirebaseAuth auth = FirebaseAuth.instance;
  @override
  Widget build(BuildContext context) {
    if (auth.currentUser != null) {
      return DashBoard();
    } else {
      return LoginPage();
    }
  }
}
