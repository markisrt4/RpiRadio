#ifndef BLUETOOTHPLAYER_H
#define BLUETOOTHPLAYER_H

#include <QDialog>

namespace Ui {
class bluetoothplayer;
}

class bluetoothplayer : public QDialog
{
    Q_OBJECT

public:
    explicit bluetoothplayer(QWidget *parent = 0);
    ~bluetoothplayer();

private:
    Ui::bluetoothplayer *ui;
};

#endif // BLUETOOTHPLAYER_H
