import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:wanderflow_app/main.dart' as app;
import 'package:wanderflow_app/screens/auth/login_screen.dart';
import 'package:wanderflow_app/screens/auth/register_screen.dart';
import 'package:wanderflow_app/screens/home/home_screen.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('端到端认证测试', () {
    testWidgets('完整注册流程测试', (WidgetTester tester) async {
      // 启动应用
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // 验证启动页面
      expect(find.byType(app.SplashScreen), findsOneWidget);
      await tester.pumpAndSettle(const Duration(seconds: 2));

      // 验证进入登录页面
      expect(find.byType(LoginScreen), findsOneWidget);

      // 点击注册按钮
      await tester.tap(find.text('注册'));
      await tester.pumpAndSettle();

      // 验证进入注册页面
      expect(find.byType(RegisterScreen), findsOneWidget);

      // 填写注册表单
      final nameField = find.byKey(const Key('name_field'));
      final emailField = find.byKey(const Key('email_field'));
      final passwordField = find.byKey(const Key('password_field'));
      final confirmPasswordField = find.byKey(const Key('confirm_password_field'));

      await tester.tap(nameField);
      await tester.enterText(nameField, '测试用户');

      await tester.tap(emailField);
      await tester.enterText(emailField, 'test_${DateTime.now().millisecondsSinceEpoch}@example.com');

      await tester.tap(passwordField);
      await tester.enterText(passwordField, 'test123456');

      await tester.tap(confirmPasswordField);
      await tester.enterText(confirmPasswordField, 'test123456');

      await tester.pumpAndSettle();

      // 点击注册按钮
      final registerButton = find.byKey(const Key('register_button'));
      await tester.tap(registerButton);
      await tester.pumpAndSettle(const Duration(seconds: 2));

      // 验证注册后的状态（可能跳转到首页或显示错误）
      // 这里需要根据实际应用逻辑调整
      expect(find.byType(RegisterScreen), findsOneWidget);
    });

    testWidgets('完整登录流程测试', (WidgetTester tester) async {
      // 启动应用
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // 确保在登录页面
      expect(find.byType(LoginScreen), findsOneWidget);

      // 填写登录表单
      final emailField = find.byKey(const Key('email_field'));
      final passwordField = find.byKey(const Key('password_field'));

      await tester.tap(emailField);
      await tester.enterText(emailField, 'existing@example.com');

      await tester.tap(passwordField);
      await tester.enterText(passwordField, 'test123456');

      await tester.pumpAndSettle();

      // 点击登录按钮
      final loginButton = find.byKey(const Key('login_button'));
      await tester.tap(loginButton);
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // 验证登录后的状态
      // 如果登录成功，应该跳转到首页
      // 如果登录失败，应该显示错误信息
      // 这里根据实际逻辑调整
    });

    testWidgets('表单验证测试', (WidgetTester tester) async {
      // 启动应用
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // 导航到注册页面
      await tester.tap(find.text('注册'));
      await tester.pumpAndSettle();

      // 测试空表单提交
      final registerButton = find.byKey(const Key('register_button'));
      await tester.tap(registerButton);
      await tester.pumpAndSettle();

      // 验证表单验证错误信息
      expect(find.text('请输入邮箱'), findsOneWidget);
      expect(find.text('请输入密码'), findsOneWidget);
      expect(find.text('请输入姓名'), findsOneWidget);

      // 测试无效邮箱
      final emailField = find.byKey(const Key('email_field'));
      await tester.tap(emailField);
      await tester.enterText(emailField, 'invalid-email');
      await tester.tap(registerButton);
      await tester.pumpAndSettle();

      expect(find.text('请输入有效的邮箱地址'), findsOneWidget);

      // 测试密码不匹配
      final nameField = find.byKey(const Key('name_field'));
      final passwordField = find.byKey(const Key('password_field'));
      final confirmPasswordField = find.byKey(const Key('confirm_password_field'));

      await tester.tap(nameField);
      await tester.enterText(nameField, '测试用户');

      await tester.tap(emailField);
      await tester.enterText(emailField, 'test@example.com');

      await tester.tap(passwordField);
      await tester.enterText(passwordField, 'password123');

      await tester.tap(confirmPasswordField);
      await tester.enterText(confirmPasswordField, 'different-password');

      await tester.tap(registerButton);
      await tester.pumpAndSettle();

      expect(find.text('两次输入的密码不一致'), findsOneWidget);
    });

    testWidgets('导航流程测试', (WidgetTester tester) async {
      // 启动应用
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // 测试登录->注册->登录导航
      expect(find.byType(LoginScreen), findsOneWidget);

      await tester.tap(find.text('注册'));
      await tester.pumpAndSettle();
      expect(find.byType(RegisterScreen), findsOneWidget);

      await tester.tap(find.text('登录'));
      await tester.pumpAndSettle();
      expect(find.byType(LoginScreen), findsOneWidget);

      // 测试忘记密码导航
      await tester.tap(find.text('忘记密码？'));
      await tester.pumpAndSettle();
      expect(find.text('忘记密码'), findsOneWidget);

      await tester.tap(find.text('返回登录'));
      await tester.pumpAndSettle();
      expect(find.byType(LoginScreen), findsOneWidget);
    });

    testWidgets('UI交互测试', (WidgetTester tester) async {
      // 启动应用
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // 测试密码可见性切换
      final passwordField = find.byKey(const Key('password_field'));
      await tester.tap(passwordField);
      await tester.enterText(passwordField, 'test123456');
      await tester.pumpAndSettle();

      final visibilityIcon = find.byKey(const Key('password_visibility_icon'));
      await tester.tap(visibilityIcon);
      await tester.pumpAndSettle();

      // 验证密码变为可见
      expect(find.text('test123456'), findsOneWidget);

      // 测试再次点击隐藏密码
      await tester.tap(visibilityIcon);
      await tester.pumpAndSettle();

      // 验证密码变为隐藏
      expect(find.text('*'), findsAtLeastNWidgets(8));
    });

    testWidgets('加载状态测试', (WidgetTester tester) async {
      // 启动应用
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // 填写表单
      final emailField = find.byKey(const Key('email_field'));
      final passwordField = find.byKey(const Key('password_field'));

      await tester.tap(emailField);
      await tester.enterText(emailField, 'test@example.com');

      await tester.tap(passwordField);
      await tester.enterText(passwordField, 'test123456');

      await tester.pumpAndSettle();

      // 点击登录按钮并观察加载状态
      final loginButton = find.byKey(const Key('login_button'));
      await tester.tap(loginButton);
      await tester.pump();

      // 验证加载指示器出现
      expect(find.byType(CircularProgressIndicator), findsOneWidget);

      // 等待加载完成
      await tester.pumpAndSettle(const Duration(seconds: 5));
    });
  });
}
