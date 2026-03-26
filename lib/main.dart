import 'bottomnav.dart';
import 'package:get/get.dart';
import 'screens/splash_screen.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'controller/index_controller.dart';
import 'package:pink/firebase_options.dart';
import 'package:pink/screens/dashboard.dart';
import 'package:pink/screens/googlemap.dart';
import 'package:pink/utilities/Mytheme.dart';
import 'package:pink/screens/chat/chathome.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:pink/screens/auth/signuppage.dart';
import 'package:stream_chat_flutter_core/stream_chat_flutter_core.dart';

// ignore_for_file: prefer_const_constructors, depend_on_referenced_packages, unused_import

Future main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  runApp(MainPage());
}

class MainPage extends StatelessWidget {
  final navigatorkey = GlobalKey<NavigatorState>();
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider<IndexController>(
          create: (_) => IndexController(),
        ),
      ],
      child: GetMaterialApp(
        //theme: ThemeData(canvasColor: CustomTheme.pinkthemecolor),
        navigatorKey: navigatorkey,
        home: SplashScreen(),
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}
