<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class settings_form
    Inherits System.Windows.Forms.Form

    'Form remplace la méthode Dispose pour nettoyer la liste des composants.
    <System.Diagnostics.DebuggerNonUserCode()> _
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
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(settings_form))
        Me.FolderBrowserDialog1 = New System.Windows.Forms.FolderBrowserDialog()
        Me.TextBox1 = New System.Windows.Forms.TextBox()
        Me.Label1 = New System.Windows.Forms.Label()
        Me.find_folder_button = New System.Windows.Forms.Button()
        Me.save_button = New System.Windows.Forms.Button()
        Me.accept_scan_checkbox = New System.Windows.Forms.CheckBox()
        Me.SuspendLayout()
        '
        'TextBox1
        '
        Me.TextBox1.Location = New System.Drawing.Point(248, 6)
        Me.TextBox1.Name = "TextBox1"
        Me.TextBox1.Size = New System.Drawing.Size(371, 23)
        Me.TextBox1.TabIndex = 0
        '
        'Label1
        '
        Me.Label1.AutoSize = True
        Me.Label1.Location = New System.Drawing.Point(6, 9)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(126, 15)
        Me.Label1.TabIndex = 1
        Me.Label1.Text = "Files download folder :"
        '
        'find_folder_button
        '
        Me.find_folder_button.Location = New System.Drawing.Point(138, 5)
        Me.find_folder_button.Name = "find_folder_button"
        Me.find_folder_button.Size = New System.Drawing.Size(104, 24)
        Me.find_folder_button.TabIndex = 2
        Me.find_folder_button.Text = "Find a folder"
        Me.find_folder_button.UseVisualStyleBackColor = True
        '
        'save_button
        '
        Me.save_button.Location = New System.Drawing.Point(13, 311)
        Me.save_button.Name = "save_button"
        Me.save_button.Size = New System.Drawing.Size(75, 23)
        Me.save_button.TabIndex = 3
        Me.save_button.Text = "Save"
        Me.save_button.UseVisualStyleBackColor = True
        '
        'accept_scan_checkbox
        '
        Me.accept_scan_checkbox.AutoSize = True
        Me.accept_scan_checkbox.Checked = True
        Me.accept_scan_checkbox.CheckState = System.Windows.Forms.CheckState.Checked
        Me.accept_scan_checkbox.Location = New System.Drawing.Point(6, 51)
        Me.accept_scan_checkbox.Name = "accept_scan_checkbox"
        Me.accept_scan_checkbox.Size = New System.Drawing.Size(173, 19)
        Me.accept_scan_checkbox.TabIndex = 8
        Me.accept_scan_checkbox.Text = "Ask before accepting a scan"
        Me.accept_scan_checkbox.UseVisualStyleBackColor = True
        '
        'settings_form
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(7.0!, 15.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(656, 346)
        Me.Controls.Add(Me.accept_scan_checkbox)
        Me.Controls.Add(Me.save_button)
        Me.Controls.Add(Me.find_folder_button)
        Me.Controls.Add(Me.Label1)
        Me.Controls.Add(Me.TextBox1)
        Me.Icon = CType(resources.GetObject("$this.Icon"), System.Drawing.Icon)
        Me.Name = "settings_form"
        Me.Text = "Settings"
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub

    Friend WithEvents FolderBrowserDialog1 As FolderBrowserDialog
    Friend WithEvents TextBox1 As TextBox
    Friend WithEvents Label1 As Label
    Friend WithEvents find_folder_button As Button
    Friend WithEvents save_button As Button
    Friend WithEvents accept_scan_checkbox As CheckBox
End Class
