<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class Form1
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
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

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.components = New System.ComponentModel.Container()
        Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(Form1))
        Me.find_ip_button = New System.Windows.Forms.Button()
        Me.TextBox1 = New System.Windows.Forms.TextBox()
        Me.Label1 = New System.Windows.Forms.Label()
        Me.copy_text_button = New System.Windows.Forms.Button()
        Me.save_text_button = New System.Windows.Forms.Button()
        Me.help_button = New System.Windows.Forms.Button()
        Me.SaveFileDialog1 = New System.Windows.Forms.SaveFileDialog()
        Me.BackgroundWorker1 = New System.ComponentModel.BackgroundWorker()
        Me.clear_output_button = New System.Windows.Forms.Button()
        Me.Timer1 = New System.Windows.Forms.Timer(Me.components)
        Me.settings_button = New System.Windows.Forms.Button()
        Me.SuspendLayout()
        '
        'find_ip_button
        '
        Me.find_ip_button.Font = New System.Drawing.Font("Segoe UI Semibold", 9.0!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point)
        Me.find_ip_button.Location = New System.Drawing.Point(265, 11)
        Me.find_ip_button.Name = "find_ip_button"
        Me.find_ip_button.Size = New System.Drawing.Size(85, 26)
        Me.find_ip_button.TabIndex = 0
        Me.find_ip_button.Text = "QR Code"
        Me.find_ip_button.UseVisualStyleBackColor = True
        '
        'TextBox1
        '
        Me.TextBox1.Location = New System.Drawing.Point(12, 42)
        Me.TextBox1.Multiline = True
        Me.TextBox1.Name = "TextBox1"
        Me.TextBox1.Size = New System.Drawing.Size(771, 396)
        Me.TextBox1.TabIndex = 1
        '
        'Label1
        '
        Me.Label1.AutoSize = True
        Me.Label1.Font = New System.Drawing.Font("Cascadia Code SemiBold", 9.0!, CType((System.Drawing.FontStyle.Bold Or System.Drawing.FontStyle.Underline), System.Drawing.FontStyle), System.Drawing.GraphicsUnit.Point)
        Me.Label1.Location = New System.Drawing.Point(12, 17)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(112, 16)
        Me.Label1.TabIndex = 2
        Me.Label1.Text = "Scan received :"
        '
        'copy_text_button
        '
        Me.copy_text_button.Font = New System.Drawing.Font("Segoe UI Semibold", 9.0!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point)
        Me.copy_text_button.Location = New System.Drawing.Point(614, 11)
        Me.copy_text_button.Name = "copy_text_button"
        Me.copy_text_button.Size = New System.Drawing.Size(83, 26)
        Me.copy_text_button.TabIndex = 3
        Me.copy_text_button.Text = "Copy text"
        Me.copy_text_button.UseVisualStyleBackColor = True
        '
        'save_text_button
        '
        Me.save_text_button.Font = New System.Drawing.Font("Segoe UI Semibold", 9.0!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point)
        Me.save_text_button.Location = New System.Drawing.Point(536, 11)
        Me.save_text_button.Name = "save_text_button"
        Me.save_text_button.Size = New System.Drawing.Size(72, 26)
        Me.save_text_button.TabIndex = 4
        Me.save_text_button.Text = "Save text"
        Me.save_text_button.UseVisualStyleBackColor = True
        '
        'help_button
        '
        Me.help_button.Font = New System.Drawing.Font("Segoe UI Semibold", 9.0!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point)
        Me.help_button.Location = New System.Drawing.Point(451, 11)
        Me.help_button.Name = "help_button"
        Me.help_button.Size = New System.Drawing.Size(79, 26)
        Me.help_button.TabIndex = 5
        Me.help_button.Text = "How to use"
        Me.help_button.UseVisualStyleBackColor = True
        '
        'BackgroundWorker1
        '
        '
        'clear_output_button
        '
        Me.clear_output_button.Font = New System.Drawing.Font("Segoe UI Semibold", 9.0!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point)
        Me.clear_output_button.Location = New System.Drawing.Point(356, 11)
        Me.clear_output_button.Name = "clear_output_button"
        Me.clear_output_button.Size = New System.Drawing.Size(89, 26)
        Me.clear_output_button.TabIndex = 6
        Me.clear_output_button.Text = "Clear output"
        Me.clear_output_button.UseVisualStyleBackColor = True
        '
        'Timer1
        '
        Me.Timer1.Interval = 9
        '
        'settings_button
        '
        Me.settings_button.Font = New System.Drawing.Font("Segoe UI Semibold", 9.0!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point)
        Me.settings_button.Location = New System.Drawing.Point(703, 11)
        Me.settings_button.Name = "settings_button"
        Me.settings_button.Size = New System.Drawing.Size(75, 26)
        Me.settings_button.TabIndex = 8
        Me.settings_button.Text = "Settings"
        Me.settings_button.UseVisualStyleBackColor = True
        '
        'Form1
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(7.0!, 15.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.BackColor = System.Drawing.SystemColors.Highlight
        Me.ClientSize = New System.Drawing.Size(800, 450)
        Me.Controls.Add(Me.settings_button)
        Me.Controls.Add(Me.clear_output_button)
        Me.Controls.Add(Me.help_button)
        Me.Controls.Add(Me.save_text_button)
        Me.Controls.Add(Me.copy_text_button)
        Me.Controls.Add(Me.Label1)
        Me.Controls.Add(Me.TextBox1)
        Me.Controls.Add(Me.find_ip_button)
        Me.Icon = CType(resources.GetObject("$this.Icon"), System.Drawing.Icon)
        Me.Name = "Form1"
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub

    Friend WithEvents find_ip_button As Button
    Friend WithEvents TextBox1 As TextBox
    Friend WithEvents Label1 As Label
    Friend WithEvents copy_text_button As Button
    Friend WithEvents save_text_button As Button
    Friend WithEvents help_button As Button
    Friend WithEvents SaveFileDialog1 As SaveFileDialog
    Friend WithEvents BackgroundWorker1 As System.ComponentModel.BackgroundWorker
    Friend WithEvents clear_output_button As Button
    Friend WithEvents Timer1 As Timer
    Friend WithEvents settings_button As Button
End Class
