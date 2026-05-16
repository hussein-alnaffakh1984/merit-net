# دليل النشر | Deployment Guide

## 🚀 رفع الموقع على Netlify (مجاناً)

### الطريقة 1: السحب والإفلات (الأسهل) ⭐

1. اذهب إلى: **https://app.netlify.com/drop**
2. اسحب مجلد المشروع كاملاً إلى المربع
3. انتظر بضع ثوانٍ
4. ✅ موقعك جاهز! ستحصل على رابط مثل: `https://random-name-12345.netlify.app`
5. (اختياري) يمكنك تغيير الاسم من **Site settings → Change site name**

### الطريقة 2: من GitHub (للتحديثات التلقائية)

1. ارفع المشروع على GitHub (اتبع تعليمات أدناه)
2. اذهب إلى: **https://app.netlify.com/start**
3. اختر "Import from Git" → GitHub
4. اختر repository
5. اضغط "Deploy"

---

## 📦 رفع المشروع على GitHub

### الخطوات:

1. **أنشئ حساب GitHub** (إذا لم يكن لديك): https://github.com/signup

2. **أنشئ Repository جديد**:
   - اذهب إلى: https://github.com/new
   - الاسم: `merit-net`
   - الوصف: `Maternal Health Risk Prediction Pipeline`
   - اختر: **Public**
   - ❌ لا تختر "Initialize this repository"
   - اضغط "Create repository"

3. **ارفع الملفات** (افتح Terminal/CMD في مجلد المشروع):

```bash
cd merit-net-project

# تهيئة Git
git init
git add .
git commit -m "Initial commit: MERIT-Net pipeline"

# ربط بـ GitHub (استبدل YOUR-USERNAME باسمك)
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/merit-net.git
git push -u origin main
```

4. **حدّث الرابط في الورقة**:
   - افتح ورقة البحث
   - استبدل `https://github.com/[author]/merit-net`
   - بـ: `https://github.com/YOUR-USERNAME/merit-net`

---

## 🔗 ربط الموقع والـ GitHub في الورقة

### في الورقة، استبدل:

| النص الحالي | النص الجديد |
|------------|-------------|
| `https://github.com/[author]/merit-net` | `https://github.com/YOUR-USERNAME/merit-net` |
| `[email@domain.com]` | بريدك الإلكتروني |
| `[Author Names]` | Hussein Ali Hussein Al-Naffakh |
| `[University Name]` | اسم جامعتك |
| `[City]` | المدينة |

### اقتراح: أضف Live Demo في الورقة

في قسم **Code and Data Availability**:

> *"An interactive web demonstration of MERIT-Net is available at:*
> *https://YOUR-SITE.netlify.app"*

---

## ✅ Checklist قبل النشر

- [ ] رفع المشروع على GitHub
- [ ] نشر الموقع على Netlify
- [ ] تحديث الرابط في `index.html` (السطر يحتوي `[USERNAME]`)
- [ ] تحديث الرابط في `README.md`
- [ ] تحديث الرابط في الورقة (paper)
- [ ] اختبار الموقع - تأكد أن التطبيق يعمل
- [ ] إضافة وصف للـ GitHub repository

---

## 🎯 الاستخدام النهائي

في الورقة عند التقديم للمجلة، اذكر:

```
Code and Data Availability:
Source code and trained model are publicly available at:
https://github.com/YOUR-USERNAME/merit-net

An interactive web demonstration is available at:
https://YOUR-SITE.netlify.app
```

هذا سيُضيف **مصداقية كبيرة جداً** لورقتك! 🏆
