package com.tencent.wetest;

import java.lang.Thread.UncaughtExceptionHandler;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.HTTP;
import org.apache.http.util.EntityUtils;

import android.app.Activity;
import android.net.wifi.WifiManager;
import android.os.Process;
import android.util.Log;

public class WetestReport {
	public static final String TAG = "WeTestReport";
	private static final String _TAG = "wetest";

	private static WetestReport wetestReport = null;

	private static int num = 0;

	private static boolean crashInited = false;
	private static boolean report = false;

	private static UncaughtExceptionHandler defaultUncaughtExceptionHandler;

	private static void postMessage(List<NameValuePair> pairList) {
		try {
			HttpEntity requestEntity = new UrlEncodedFormEntity(pairList,
					"UTF-8");

			HttpPost httpPost = new HttpPost(
					"http://wetest.qq.com/cloudapi/api_v2/sdkreport");

			httpPost.setEntity(requestEntity);
			httpPost.setHeader(HTTP.CONTENT_TYPE,
					"application/x-www-form-urlencoded;charset=UTF-8");

			HttpClient client = new DefaultHttpClient();

			HttpResponse response = client.execute(httpPost);

			Log.d(_TAG, EntityUtils.toString(requestEntity, "UTF-8"));

			HttpEntity responseEntity = response.getEntity();

			Log.d(_TAG, EntityUtils.toString(responseEntity, "UTF-8"));

		} catch (Exception e) {
			Log.e(_TAG, e.getMessage(), e);
		}
	}

	private static void getVersion() {
		if (report) {
			return;
		}
		try {
			List<NameValuePair> params = new ArrayList<NameValuePair>();
			String packageName = "";
			int ipAddress = 0;
			String fingerPrint = "";
			report = true;
			Activity activity = U3DAutomation.GetPlayerActivity();
			try {
				packageName = activity.getApplicationContext().getPackageName();
			} catch (Exception e) {
			}

			try {
				WifiManager wifiManager = (WifiManager) activity
						.getSystemService(Activity.WIFI_SERVICE);
				ipAddress = wifiManager.getConnectionInfo().getIpAddress();
			} catch (Exception e) {
			}

			String model = android.os.Build.MODEL;
			Integer version = android.os.Build.VERSION.SDK_INT;
			fingerPrint = android.os.Build.FINGERPRINT;

			MessageDigest md5 = MessageDigest.getInstance("MD5");
			md5.update(packageName.getBytes());
			byte[] messageDigest = md5.digest();
			StringBuilder hexString = new StringBuilder();
			for (byte aMessageDigest : messageDigest) {
				String h = Integer.toHexString(0xFF & aMessageDigest);
				while (h.length() < 2)
					h = "0" + h;
				hexString.append(h);
			}

			String mdPackage = hexString.toString();

			Log.i(_TAG, "PackageName:" + packageName + "(" + mdPackage
					+ ") Host:" + ipAddress + " model:" + model + " version:"
					+ version + " FingerInt:" + fingerPrint);

			params.add(new BasicNameValuePair("packagename", mdPackage));
			params.add(new BasicNameValuePair("ip", Integer.toString(ipAddress)));
			params.add(new BasicNameValuePair("model", model));
			// params.add(new BasicNameValuePair("version",
			// Integer.toString(version)));
			params.add(new BasicNameValuePair("fingerprint", fingerPrint));

			postMessage(params);
		} catch (Exception e) {
			Log.e(TAG, e.getMessage(), e);
		}

	}

	static {
		getVersion();
	}

	private static UncaughtExceptionHandler _uncaughtExceptionHandler = new UncaughtExceptionHandler() {

		@Override
		public void uncaughtException(Thread thread, Throwable ex) {
			try {
				String type = ex.getClass().getCanonicalName();

				String message = ex.getMessage();
				StackTraceElement[] elements = ex.getStackTrace();

				StringBuilder stackTrace = new StringBuilder();
				stackTrace.append(ex.toString()).append("\n");
				for (StackTraceElement stackTraceElement : elements) {
					stackTrace.append(stackTraceElement.toString())
							.append("\n");
				}

				StringBuilder sb = new StringBuilder();
				sb.append("*****************<WetestReport>*********************\n");
				sb.append("EXCEPTION TYPE: ");
				sb.append(type).append("\n");

				sb.append("MESSAGE: ");
				sb.append(message).append("\n");

				sb.append("STACKTRACE: \n");
				sb.append(stackTrace).append("\n\n");

				sb.append("SCENE: ");
				sb.append("").append("\n");

				sb.append("UNCAUGHT: ");
				sb.append("True").append("\n");

				sb.append("CRASH TYPE: ");
				sb.append("JAVA CRASH\n");

				sb.append("INDEX: ");
				sb.append(num++);
				sb.append("\n");

				sb.append("***************************************************\n");

				Log.e(TAG, sb.toString());

				Thread.sleep(100);
			} catch (Exception e) {
				Log.d(_TAG, "WetestReport error handler uncaught exception");
			}

			defaultUncaughtExceptionHandler.uncaughtException(thread, ex);

		}
	};

	public static void testCrash() {

		Log.e(_TAG, "TestCrash");
		Activity localActivity;
		try {
			localActivity = U3DAutomation.GetPlayerActivity();
			if (localActivity == null) {
				Log.e(_TAG, "Can not find UnityActivity");
				return;
			} else {
				localActivity.runOnUiThread(new Runnable() {

					@Override
					public void run() {
						Log.i(_TAG, "Try to crash Main UI");
						int a = 0, b = 1, z = 0;
						z = b / a;
					}
				});
			}
		} catch (Exception e) {
			// TODO: handle exception
		}

	}

	/*
	 * private Context getApplicationContext() { if (context == null) { Activity
	 * localActivity; if ((localActivity = U3DAutomation.GetPlayerActivity()) !=
	 * null) { context = localActivity.getApplicationContext(); } } return
	 * context; }
	 */

	// public static WetestReport getInstance(){
	// Log.d(_TAG, "getInstance");
	// if (wetestReport == null) {
	// wetestReport = new WetestReport();
	// }
	// return wetestReport;
	// }

	public static void initCrashReport() {
		if (crashInited) {
			Log.d(_TAG, "java crash monitor has inited");
			return;
		}
		try {
			Log.i(_TAG, "Register java uncaught exception");
			defaultUncaughtExceptionHandler = Thread
					.getDefaultUncaughtExceptionHandler();
			Thread.setDefaultUncaughtExceptionHandler(_uncaughtExceptionHandler);
			crashInited = true;
		} catch (Exception e) {
			// TODO: handle exception
		}
	}

	private static void exitApplication() {
		int i = Process.myPid();
		Log.e(TAG, "Exit application by kill process " + i);
		Process.killProcess(i);
	}

	public static void logAgent(String content) {
		Log.d(TAG, content);
	}

	public static void logError(String type, String message, String stackTrace,
			String scene, boolean uncaught) {
		if (type == null)
			type = "";
		if (message == null)
			message = "";
		if (stackTrace == null)
			stackTrace = "";
		if (scene == null)
			scene = "";
		StringBuilder sb = new StringBuilder();
		sb.append("*****************<WetestReport>*********************\n");
		sb.append("EXCEPTION TYPE: ");
		sb.append(type).append("\n");

		sb.append("MESSAGE: ");
		sb.append(message).append("\n");

		sb.append("STACKTRACE: \n");
		sb.append(stackTrace).append("\n\n");

		sb.append("SCENE: ");
		sb.append(scene).append("\n");

		sb.append("UNCAUGHT: ");
		sb.append(uncaught ? "True" : "False").append("\n");

		sb.append("CRASH TYPE: ");
		sb.append("C# CRASH\n");

		sb.append("INDEX: ");
		sb.append(num++);
		sb.append("\n");

		sb.append("***************************************************\n");

		// 一定要使用Error级别的，部分手机会自动过滤掉Debug级别的日志
		Log.e(TAG, sb.toString());
	}
}
