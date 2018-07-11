import QtQuick 2.10
import QtQuick.Controls 2.1
import QtQuick.Window 2.2
import QtQuick.Controls.Material 2.3


ApplicationWindow {
    id: applicationWindow
    Material.theme: Material.Light
    title: qsTr("Test Invoke")
    visible: true

    width: 600
    height: 500

    ComboBox {
        id: comboBox
        width: 200
        model: Manager.stations
    }
}