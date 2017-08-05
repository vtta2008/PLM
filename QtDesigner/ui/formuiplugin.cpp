#include "formui.h"
#include "formuiplugin.h"

#include <QtPlugin>

FormUIPlugin::FormUIPlugin(QObject *parent)
    : QObject(parent)
{
    m_initialized = false;
}

void FormUIPlugin::initialize(QDesignerFormEditorInterface * /* core */)
{
    if (m_initialized)
        return;

    // Add extension registrations, etc. here

    m_initialized = true;
}

bool FormUIPlugin::isInitialized() const
{
    return m_initialized;
}

QWidget *FormUIPlugin::createWidget(QWidget *parent)
{
    return new FormUI(parent);
}

QString FormUIPlugin::name() const
{
    return QLatin1String("FormUI");
}

QString FormUIPlugin::group() const
{
    return QLatin1String("");
}

QIcon FormUIPlugin::icon() const
{
    return QIcon();
}

QString FormUIPlugin::toolTip() const
{
    return QLatin1String("");
}

QString FormUIPlugin::whatsThis() const
{
    return QLatin1String("");
}

bool FormUIPlugin::isContainer() const
{
    return false;
}

QString FormUIPlugin::domXml() const
{
    return QLatin1String("<widget class=\"FormUI\" name=\"formUI\">\n</widget>\n");
}

QString FormUIPlugin::includeFile() const
{
    return QLatin1String("formui.h");
}
#if QT_VERSION < 0x050000
Q_EXPORT_PLUGIN2(formuiplugin, FormUIPlugin)
#endif // QT_VERSION < 0x050000
