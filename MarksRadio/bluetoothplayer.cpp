#include "bluetoothplayer.h"
#include "ui_bluetoothplayer.h"

bluetoothplayer::bluetoothplayer(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::bluetoothplayer)
{
    ui->setupUi(this);
}

bluetoothplayer::~bluetoothplayer()
{
    delete ui;
}
