#include "vncviewer.h"
#include "ui_vncviewer.h"

VncViewer::VncViewer(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::VncViewer)
{
    ui->setupUi(this);
}

VncViewer::~VncViewer()
{
    delete ui;
}
