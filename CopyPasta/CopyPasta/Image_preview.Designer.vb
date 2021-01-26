<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()>
Partial Class Image_preview
    Inherits System.Windows.Forms.Form

    'Form remplace la méthode Dispose pour nettoyer la liste des composants.
    <System.Diagnostics.DebuggerNonUserCode()>
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Requise par le Concepteur Windows Form
    Private components As System.ComponentModel.IContainer

    'REMARQUE : la procédure suivante est requise par le Concepteur Windows Form
    'Elle peut être modifiée à l'aide du Concepteur Windows Form.  
    'Ne la modifiez pas à l'aide de l'éditeur de code.
    <System.Diagnostics.DebuggerStepThrough()>
    Private Sub InitializeComponent()
        Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(Image_preview))
        Me.PictureBox1 = New System.Windows.Forms.PictureBox()
        Me.save_button = New System.Windows.Forms.Button()
        Me.SaveFileDialog1 = New System.Windows.Forms.SaveFileDialog()
        Me.save_in_different_folder = New System.Windows.Forms.Button()
        CType(Me.PictureBox1, System.ComponentModel.ISupportInitialize).BeginInit()
        Me.SuspendLayout()
        '
        'PictureBox1
        '
        Me.PictureBox1.Location = New System.Drawing.Point(3, 2)
        Me.PictureBox1.Name = "PictureBox1"
        Me.PictureBox1.Size = New System.Drawing.Size(308, 177)
        Me.PictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.AutoSize
        Me.PictureBox1.TabIndex = 0
        Me.PictureBox1.TabStop = False
        '
        'save_button
        '
        Me.save_button.BackColor = System.Drawing.Color.MediumSpringGreen
        Me.save_button.FlatStyle = System.Windows.Forms.FlatStyle.Popup
        Me.save_button.Location = New System.Drawing.Point(3, 185)
        Me.save_button.Name = "save_button"
        Me.save_button.Size = New System.Drawing.Size(80, 23)
        Me.save_button.TabIndex = 1
        Me.save_button.Text = "Save Image"
        Me.save_button.UseVisualStyleBackColor = False
        '
        'save_in_different_folder
        '
        Me.save_in_different_folder.BackColor = System.Drawing.Color.Aquamarine
        Me.save_in_different_folder.FlatStyle = System.Windows.Forms.FlatStyle.Popup
        Me.save_in_different_folder.Location = New System.Drawing.Point(89, 185)
        Me.save_in_different_folder.Name = "save_in_different_folder"
        Me.save_in_different_folder.Size = New System.Drawing.Size(191, 23)
        Me.save_in_different_folder.TabIndex = 2
        Me.save_in_different_folder.Text = "Save Image in a different folder"
        Me.save_in_different_folder.UseVisualStyleBackColor = False
        '
        'Image_preview
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(7.0!, 15.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(800, 450)
        Me.Controls.Add(Me.save_in_different_folder)
        Me.Controls.Add(Me.save_button)
        Me.Controls.Add(Me.PictureBox1)
        Me.Icon = CType(resources.GetObject("$this.Icon"), System.Drawing.Icon)
        Me.Name = "Image_preview"
        Me.Text = "Image_preview"
        CType(Me.PictureBox1, System.ComponentModel.ISupportInitialize).EndInit()
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub

    Friend WithEvents PictureBox1 As PictureBox
    Friend WithEvents save_button As Button
    Friend WithEvents SaveFileDialog1 As SaveFileDialog
    Friend WithEvents save_in_different_folder As Button
End Class
