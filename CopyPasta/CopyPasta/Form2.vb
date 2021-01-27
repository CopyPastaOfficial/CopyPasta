Public Class settings_form
    Private Sub settings_form_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        TextBox1.Text = My.Computer.FileSystem.ReadAllText("download_dir.Blue")
    End Sub

    Private Sub find_folder_button_Click(sender As Object, e As EventArgs) Handles find_folder_button.Click
        FolderBrowserDialog1.ShowDialog()
        TextBox1.Text = FolderBrowserDialog1.SelectedPath
    End Sub

    Private Sub save_button_Click(sender As Object, e As EventArgs) Handles save_button.Click
        My.Computer.FileSystem.WriteAllText("download_dir.Blue", TextBox1.Text, False)
    End Sub

    Private Sub accept_scan_checkbox_CheckedChanged(sender As Object, e As EventArgs) Handles accept_scan_checkbox.CheckedChanged
        If accept_scan_checkbox.Checked Then
            My.Computer.FileSystem.WriteAllText("ask_scan.Blue", "", False)
        Else
            My.Computer.FileSystem.DeleteFile("ask_scan.Blue")
        End If
    End Sub


End Class