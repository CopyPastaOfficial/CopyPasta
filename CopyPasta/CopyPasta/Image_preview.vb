Public Class Image_preview
    Private Sub Image_preview_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        PictureBox1.Image = Image.FromFile("temp.jpeg")
    End Sub

    Private Sub save_in_different_folder_Click(sender As Object, e As EventArgs) Handles save_in_different_folder.Click
        SaveFileDialog1.Filter = "JPEG Files (*.jpeg*)|*.jpeg"
        If SaveFileDialog1.ShowDialog = Windows.Forms.DialogResult.OK Then
            PictureBox1.Image.Save(SaveFileDialog1.FileName)
        End If
    End Sub

    Private Sub save_button_Click(sender As Object, e As EventArgs) Handles save_button.Click
        PictureBox1.Image.Save("scan" & (CInt(Int((10000000 * Rnd()) + 1))).ToString & ".jpeg")
    End Sub

    Private Sub Image_preview_CLose(ByVal sender As Object, ByVal e As System.Windows.Forms.FormClosingEventArgs) Handles Me.FormClosing
        If My.Computer.FileSystem.FileExists("tmppic.jpeg") Then
            My.Computer.FileSystem.DeleteFile("tmppic.jpeg")

        End If

    End Sub

End Class