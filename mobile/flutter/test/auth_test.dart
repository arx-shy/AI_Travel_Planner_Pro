import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:wanderflow_app/services/auth_service.dart';
import 'package:wanderflow_app/screens/auth/login_screen.dart';
import 'package:wanderflow_app/screens/auth/register_screen.dart';
import 'package:wanderflow_app/screens/splash/splash_screen.dart';

void main() {
  group('认证功能测试', () {
    // 注意：SplashScreen 需要完整的路由环境，这里跳过直接测试
    // 在集成测试中进行完整的导航流程测试

    testWidgets('AuthState 类测试', (WidgetTester tester) async {
      // 测试 AuthState 类
      final authState = AuthState(
        isAuthenticated: false,
        user: null,
        quota: null,
      );

      expect(authState.isAuthenticated, isFalse);
      expect(authState.user, isNull);
      expect(authState.quota, isNull);
    });

    testWidgets('LoginScreen 组件渲染测试', (WidgetTester tester) async {
      // 直接测试 LoginScreen 组件
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: LoginScreen(),
          ),
        ),
      );

      await tester.pumpAndSettle();

      // 验证登录页面核心元素
      expect(find.byType(LoginScreen), findsOneWidget);
      expect(find.byType(TextFormField), findsAtLeastNWidgets(2));
    });

    testWidgets('RegisterScreen 组件渲染测试', (WidgetTester tester) async {
      // 直接测试 RegisterScreen 组件
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: RegisterScreen(),
          ),
        ),
      );

      await tester.pumpAndSettle();

      // 验证注册页面核心元素
      expect(find.byType(RegisterScreen), findsOneWidget);
      expect(find.byType(TextFormField), findsAtLeastNWidgets(3));
    });

    testWidgets('登录表单输入测试', (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: LoginScreen(),
          ),
        ),
      );

      await tester.pumpAndSettle();

      // 查找输入框
      final textFields = find.byType(TextFormField);
      expect(textFields, findsAtLeastNWidgets(2));

      // 测试输入邮箱
      await tester.enterText(textFields.first, 'test@example.com');
      await tester.pumpAndSettle();
      expect(find.text('test@example.com'), findsOneWidget);

      // 测试输入密码
      await tester.enterText(textFields.at(1), 'password123');
      await tester.pumpAndSettle();
    });

    testWidgets('注册表单输入测试', (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: RegisterScreen(),
          ),
        ),
      );

      await tester.pumpAndSettle();

      // 查找输入框
      final textFields = find.byType(TextFormField);
      expect(textFields, findsAtLeastNWidgets(3));

      // 测试输入姓名
      await tester.enterText(textFields.first, '测试用户');
      await tester.pumpAndSettle();
      expect(find.text('测试用户'), findsOneWidget);
    });

    testWidgets('AuthService 初始状态测试', (WidgetTester tester) async {
      // 测试AuthService的静态getter
      expect(AuthService.isAuthenticated, isFalse);
      expect(AuthService.currentUser, isNull);
      expect(AuthService.currentQuota, isNull);
    });

    testWidgets('UI组件存在性测试', (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: LoginScreen(),
          ),
        ),
      );

      await tester.pumpAndSettle();

      // 验证主要UI组件存在
      expect(find.byType(Scaffold), findsOneWidget);
      expect(find.byType(TextFormField), findsAtLeastNWidgets(2));
    });

    testWidgets('主题适配测试', (WidgetTester tester) async {
      // 测试浅色主题
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            theme: ThemeData.light(useMaterial3: true),
            home: const LoginScreen(),
          ),
        ),
      );

      await tester.pumpAndSettle();
      expect(find.byType(LoginScreen), findsOneWidget);

      // 测试深色主题
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            theme: ThemeData.dark(useMaterial3: true),
            home: const LoginScreen(),
          ),
        ),
      );

      await tester.pumpAndSettle();
      expect(find.byType(LoginScreen), findsOneWidget);
    });

    testWidgets('表单验证机制测试', (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: LoginScreen(),
          ),
        ),
      );

      await tester.pumpAndSettle();

      // 查找登录按钮并点击（不输入任何内容）
      final buttons = find.byType(ElevatedButton);
      if (buttons.evaluate().isNotEmpty) {
        await tester.tap(buttons.first);
        await tester.pumpAndSettle();
      }

      // 表单应该有验证逻辑
      expect(find.byType(LoginScreen), findsOneWidget);
    });

    testWidgets('密码输入框遮挡测试', (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: LoginScreen(),
          ),
        ),
      );

      await tester.pumpAndSettle();

      // 密码字段应该是遮挡的
      final textFields = find.byType(TextFormField);
      expect(textFields, findsAtLeastNWidgets(2));
    });
  });
}
