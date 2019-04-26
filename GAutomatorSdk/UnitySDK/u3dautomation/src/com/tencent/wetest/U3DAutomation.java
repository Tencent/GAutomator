package com.tencent.wetest;

import java.lang.reflect.Field;
import java.lang.reflect.Method;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.os.Build;
import android.os.SystemClock;
import android.util.Log;
import android.view.InputDevice;
import android.view.MotionEvent;
import android.view.SurfaceView;
import android.view.View;

public class U3DAutomation {

	private final static String TAG = "wetest";
	protected static View mUnityPlayer = null;
	protected static boolean handleForward = false;
	protected static Class<?> unityPlayerClass = null;
	protected static Field forward = null;
	protected static int unity_version = 0;
	protected static Method nativeForwardEventsToDalvik = null;

	protected static Activity playerActivity = null;
	protected static SurfaceView surfaceView = null; //unity SurfaceView field
	protected static Context scontext = null;
	protected static MScreen mscreen = null;

	protected static class MScreen {
		public int width = 0;
		public int height = 0;
		public float x = 0;
		public float y = 0;
		MScreen() {
			width = 0;
			height = 0;
			x = 0;
			y = 0;
		}

		MScreen(int w, int h, float x, float y) {
			width = w;
			height = h;
			this.x = x;
			this.y = y;
		}
	}

	static class InjectAction implements Runnable {

		private MotionEvent event;
		private View v = null;

		public InjectAction(MotionEvent event, View view) {
			this.event = event;
			this.v = view;
		}

		@Override
		public void run() {

			while (true) {
				if (handleForward) {
					setForward(false);
					if (!v.onTouchEvent(event)) {
						Log.e(TAG, "touch fail.");
					}

					setForward(true);
					break;
				}

				boolean result = v.onTouchEvent(event);

				if (!result) {
					boolean forwardResult = getForward();
					Log.i(TAG, "getForward = " + forwardResult);

					if (forwardResult) {
						handleForward = true;
						continue;
					}
				}

				break;
			}

			event.recycle();
		}
	}

	private static int getUnityVersion() {
		try {

			Field f = getDeclaredFieldNest(unityPlayerClass, "l");

			if (f != null) {
				f.setAccessible(true);

				if (f.getGenericType().equals(boolean.class)) {
					return 4;
				}
			}

			f = getDeclaredFieldNest(unityPlayerClass, "k");

			if (f != null) {
				f.setAccessible(true);

				if (f.getGenericType().equals(boolean.class)) {
					return 5;
				}
			}

			return 0;

		} catch (NoSuchFieldException e) {
			Log.e(TAG, e.getMessage(),e);
		}

		return 0;
	}

	private static boolean getForward() {

		try {

			if (forward == null) {

				String fname = "";
				if (unity_version == 5) {
					fname = "k";
				} else if (unity_version == 4) {
					fname = "l";
				} else {
					return false;
				}

				forward = getDeclaredFieldNest(unityPlayerClass, fname);

				if (forward == null) {
					Log.e(TAG, "can't find forwardNative!");
					return false;
				}

				forward.setAccessible(true);
			}

			return forward.getBoolean(mUnityPlayer);

		} catch (NoSuchFieldException e) {
			Log.e(TAG, "getForward", e);
		} catch (IllegalAccessException e) {
			Log.e(TAG, "getForward", e);
		} catch (IllegalArgumentException e) {
			Log.e(TAG, "getForward", e);
		}

		return false;

	}

	private static void setForward(boolean b) {
		try {
			if (unity_version == 4) {
				if (forward == null) {
					forward = getDeclaredFieldNest(unityPlayerClass, "l");

					if (forward == null) {
						Log.e(TAG, "can't find forwardNative!");
						return;
					}

					forward.setAccessible(true);
				}

				forward.setBoolean(mUnityPlayer, b);
			}

			try {
				if (nativeForwardEventsToDalvik == null) {
					nativeForwardEventsToDalvik = unityPlayerClass
							.getDeclaredMethod("nativeForwardEventsToDalvik",
									boolean.class);

					if (nativeForwardEventsToDalvik == null) {
						Log.e(TAG, "can't find nativeForwardEventsToDalvik!");
						return;
					}

					nativeForwardEventsToDalvik.setAccessible(true);
				}

				nativeForwardEventsToDalvik.invoke(mUnityPlayer, b);
			} catch (Exception e) {
				Log.e(TAG, "can't find nativeForwardEventsToDalvik!");
			}
			return;

		} catch (NoSuchFieldException e) {
			Log.e(TAG, "setForward", e);
		} catch (IllegalAccessException e) {
			Log.e(TAG, "setForward", e);
		} catch (IllegalArgumentException e) {
			Log.e(TAG, "setForward", e);
		}
	}

	private static Field getDeclaredFieldNest(Class<?> cls, String name)
			throws NoSuchFieldException {

		NoSuchFieldException ex = null;

		try {
			return cls.getDeclaredField(name);
		} catch (NoSuchFieldException e) {
			ex = e;
		}

		Class<?> supercls = cls.getSuperclass();

		if (supercls == null) {
			throw ex;
		}

		return getDeclaredFieldNest(supercls, name);
	}

	private static Class<?> getUnityPlayerClass() {
		if (unityPlayerClass != null) {
			return unityPlayerClass;
		}

		try {
			unityPlayerClass = Class.forName("com.unity3d.player.UnityPlayer");
			return unityPlayerClass;
		} catch (ClassNotFoundException e) {
			Log.e(TAG, "can't find com.unity3d.player.UnityPlayer");
		}

		return null;
	}

	@SuppressLint({ "NewApi", "Recycle" })
	public static void InjectTouchEvent(int action, float x, float y) {
		long now = SystemClock.uptimeMillis();

		final float DEFAULT_SIZE = 1.0f;
		final int DEFAULT_META_STATE = 0;
		final float DEFAULT_PRECISION_X = 1.0f;
		final float DEFAULT_PRECISION_Y = 1.0f;
		final int DEFAULT_DEVICE_ID = 0;
		final int DEFAULT_EDGE_FLAGS = 0;

		float pressure = (action == MotionEvent.ACTION_UP) ? 0.0f : 1.0f;

		MotionEvent event = MotionEvent.obtain(now, now, action, x, y,
				pressure, DEFAULT_SIZE, DEFAULT_META_STATE,
				DEFAULT_PRECISION_X, DEFAULT_PRECISION_Y, DEFAULT_DEVICE_ID,
				DEFAULT_EDGE_FLAGS);

		if (Build.VERSION.SDK_INT >= 12) {
			event.setSource(InputDevice.SOURCE_TOUCHSCREEN);
		}

		View unityPlayer = (View)getUnityPlayerActivity();

		if (unityPlayer == null) {
			Log.e(TAG,
					"Unable to get UnityPlayer object! please check the Unity3D version.");
		} else {

			if (unity_version == 0) {
				unity_version = getUnityVersion();
				Log.i(TAG, "Unity version = " + unity_version);
			}

			unityPlayer.post(new InjectAction(event, unityPlayer));
		}
	}

	public static Activity GetPlayerActivity() {
		if (playerActivity != null) {
			return playerActivity;
		}

		try {
			Class<?> unityPlayerClass = getUnityPlayerClass();
			if (unityPlayerClass == null) {
				Log.e(TAG,
						"GetPlayerActivity: can't find com.unity3d.player.UnityPlayer");
				return null;
			}

			Field fcurrentActivity = getDeclaredFieldNest(unityPlayerClass,
					"currentActivity");
			if (fcurrentActivity == null) {
				Log.e(TAG, "GetPlayerActivity: can't find currentActivity");
				return null;
			}

			Object objcurrentActivity = fcurrentActivity.get(null);

			if (objcurrentActivity == null) {
				Log.e(TAG, "GetPlayerActivity: can't get currentActivity");
				return null;
			}

			playerActivity = (Activity) objcurrentActivity;
			
		} catch (Exception e) {
			Log.e(TAG, e.getMessage(), e);
		}

		return playerActivity;
	}

	private static Object getUnityPlayerActivity() {
		Activity obj = (Activity) GetPlayerActivity();
		if (obj == null) {
			return null;
		}
		try {
			if (obj.getClass().getCanonicalName()
					.equals("com.unity3d.player.UnityPlayer")) {
				return obj;
			} else {
				Log.i(TAG, "Activity obj name= "+obj.getClass().getCanonicalName());
				
				Field[] fields = obj.getClass().getDeclaredFields();

				for (int i = 0; i < fields.length; ++i) {
					Field f = fields[i];
					Log.i(TAG, "field type = " + f.getType());
					if (f.getType().getCanonicalName()
							.equals("com.unity3d.player.UnityPlayer")) {
						Object activity;
						try {
							f.setAccessible(true);
							activity = f.get(obj);
							return activity;
						} catch (IllegalAccessException e) {
							Log.e(TAG, e.getMessage(), e);
						} catch (IllegalArgumentException e) {
							Log.e(TAG, e.getMessage(), e);
						}

					}
				}
				
			}
		} catch (Exception e) {
			Log.e(TAG, e.getMessage(), e);
		}

		return null;
	}
	
	
	private static SurfaceView getSurfaceView(){
		if (surfaceView == null) {
			Object activity = getUnityPlayerActivity();
			if (activity == null) {
				Log.e(TAG, "not find com.unity3d.player.UnityPlayer");
				return null;
			}
			
			Field[] fields = activity.getClass().getDeclaredFields();

			for (int i = 0; i < fields.length; ++i) {
				Field f = fields[i];
				Log.i(TAG, "field type = " + f.getType());
				if (f.getType() == SurfaceView.class) {
					Log.i(TAG, "find SurfaceView");
					f.setAccessible(true);
					try {
						surfaceView = (SurfaceView) f.get(activity);
						
					} catch (IllegalAccessException e) {
						Log.e(TAG, e.getMessage());
					} catch (IllegalArgumentException e) {
						Log.e(TAG, e.getMessage());
					}
				}
			}
		}
		return surfaceView;
	}
	
	/**
	 * @brief 
	 * 
	 * use Surfaceview to get the unity application's display size
	 * 
	 * @note 
	 * @return
	 */
	private static MScreen getMscreen() {
		SurfaceView surfaceView_ = getSurfaceView();
		if(surfaceView_!=null){
			try {
				int[] rootViewLocation = new int[2];
				surfaceView_.getLocationOnScreen(rootViewLocation);
				float x = rootViewLocation[0];
				float y = rootViewLocation[1];
				int height = surfaceView_.getHeight();
				int width = surfaceView_.getWidth();
				mscreen = new MScreen(width, height,x,y);
				return mscreen;
			} catch (Exception e) {
				Log.e(TAG, e.getMessage());
			}
		}

		//can't find surfaceview use other method
		return GetMResolution();
	}

	/**
	 * @brief 
	 * 
	 * use the activity's root component to get the display size
	 * 
	 * @note 
	 * 
	 * wrong in some mobile phone
	 * 
	 * @return
	 */
	private static MScreen GetMResolution() {
		Log.i(TAG, "GetMResolution Enter");

		Activity obj = (Activity) GetPlayerActivity();
		if (obj == null) {
			Log.e(TAG, "GetContext: get activity is null");
			return null;
		}

		scontext = (Context) obj;

		View view = (View) obj.findViewById(android.R.id.content);

		Log.d(TAG, "View class name = " + view.getClass().getCanonicalName());
		int width = view.getWidth();
		int height = view.getHeight();
		int[] rootViewLocation = new int[2];
		view.getLocationOnScreen(rootViewLocation);
		float x = rootViewLocation[0];
		float y = rootViewLocation[1];

		Log.d(TAG, "width=" + width + ", height=" + height + ", x=" + x + ", y=" + y);

		mscreen = new MScreen(width, height, x , y);

		return mscreen;
	}

	public static int GetWidth() {
		Log.i(TAG, "GetWidth()");
		MScreen msc = null;
		try {
			msc = getMscreen(); //鏂瑰紡1
			return msc.width;
		} catch (Exception e) {
			Log.e(TAG, e.getMessage(),e);
		}
		
		return -1;
		

	}

	public static int GetHeight() {
		MScreen msc = null;
		try {
			msc = getMscreen();
			return msc.height;
		} catch (Exception e) {
			Log.e(TAG, e.getMessage(),e);
		}
		return -1;
	}
	
	public static float GetX() {
		Log.i(TAG, "GetX()");
		MScreen msc = null;
		try {
			msc = getMscreen(); //鏂瑰紡1
			return msc.x;
		} catch (Exception e) {
			Log.e(TAG, e.getMessage(),e);
		}
		return -1;
	}
	
	public static float GetY() {
		Log.i(TAG, "GetY()");
		MScreen msc = null;
		try {
			msc = getMscreen(); //鏂瑰紡1
			return msc.y;
		} catch (Exception e) {
			Log.e(TAG, e.getMessage(),e);
		}
		return -1;
	}

}
