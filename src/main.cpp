#include <QtQml/QQmlApplicationEngine>
#include <QtGui/QGuiApplication>

#include <QtQuick/QQuickView>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    QQmlApplicationEngine engine;

    const QUrl url(QStringLiteral("qrc:/MainWindow.qml"));
    QObject::connect(&engine, &QQmlApplicationEngine::objectCreated,
                     &app, [url](QObject *obj, const QUrl &objUrl) {
        if (!obj && url == objUrl)
            QCoreApplication::exit(-1);
    }, Qt::QueuedConnection);
    engine.load(url);

    return app.exec();

//    QGuiApplication app(argc, argv);
//    QQuickView view;
//    view.setSource(QUrl("qrc:/MainWindow.qml"));
//    view.show();
//    return app.exec();

}
