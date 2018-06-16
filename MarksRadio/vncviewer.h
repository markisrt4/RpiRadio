#ifndef VNCVIEWER_H
#define VNCVIEWER_H

#include <QDialog>

namespace Ui {
class VncViewer;
}

class VncViewer : public QDialog
{
    Q_OBJECT

public:
    explicit VncViewer(QWidget *parent = 0);
    ~VncViewer();

private:
    Ui::VncViewer *ui;
};

#endif // VNCVIEWER_H
