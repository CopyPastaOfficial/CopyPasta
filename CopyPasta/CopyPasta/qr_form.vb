Public Class qr_form
    Private Sub qr_form_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        PictureBox1.Image = Image.FromFile("qr.jpeg")
    End Sub

End Class