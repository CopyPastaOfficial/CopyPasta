Imports System.Net.Sockets
Imports System.Text
Imports System.Net.NetworkInformation

Public Class Form1
    Dim text = ""
    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        BackgroundWorker1.RunWorkerAsync()
        My.Computer.FileSystem.WriteAllText("tmp.Blue", "", False)

        My.Computer.FileSystem.WriteAllText("ask_scan.Blue", "", False)

        If Not My.Computer.FileSystem.FileExists("download_dir.Blue") Then
            My.Computer.FileSystem.WriteAllText("download_dir.Blue", "C:\Users\" & Environment.UserName & "\Downloads\", False)
        End If


        Timer1.Start()

    End Sub

    Private Sub help_button_Click(sender As Object, e As EventArgs) Handles help_button.Click
        Dim webAddress As String = "https://www.github.com/thaaoblues/"
        RunCommand("start", "msedge " & webAddress, False)
    End Sub

    Private Sub save_text_button_Click(sender As Object, e As EventArgs) Handles save_text_button.Click
        SaveFileDialog1.Filter = "TXT Files (*.txt*)|*.txt"
        If SaveFileDialog1.ShowDialog = Windows.Forms.DialogResult.OK Then
            My.Computer.FileSystem.WriteAllText(SaveFileDialog1.FileName, TextBox1.Text, True)
        End If
    End Sub

    Private Sub copy_text_button_Click(sender As Object, e As EventArgs) Handles copy_text_button.Click
        My.Computer.Clipboard.Clear()
        My.Computer.Clipboard.SetText(TextBox1.Text)
    End Sub

    Private Sub find_ip_button_Click(sender As Object, e As EventArgs) Handles find_ip_button.Click


        Dim GetIPv4Address As String
        GetIPv4Address = String.Empty
        Dim strHostName As String = System.Net.Dns.GetHostName()
        Dim iphe As System.Net.IPHostEntry = System.Net.Dns.GetHostEntry(strHostName)

        For Each ipheal As System.Net.IPAddress In iphe.AddressList
            If ipheal.AddressFamily = System.Net.Sockets.AddressFamily.InterNetwork Then
                GetIPv4Address = ipheal.ToString()
            End If
        Next

        Dim nics() As NetworkInterface = NetworkInterface.GetAllNetworkInterfaces()
        Dim mac = nics(1).GetPhysicalAddress.ToString
        mac = mac(0) + mac(1) + ":" + mac(2) + mac(3) + ":" + mac(4) + mac(5) + ":" + mac(6) + mac(7) + ":" + mac(8) + mac(9) + ":" + mac(10) + mac(11)
        Using client As New System.Net.WebClient()

            client.DownloadFile("https://chart.googleapis.com/chart?cht=qr&chs=150x150&chl=" & GetIPv4Address, "qr.jpeg")
        End Using

        Threading.Thread.Sleep(1000)
        qr_form.Show()

    End Sub





    Private Sub BackgroundWorker1_DoWork(sender As Object, e As System.ComponentModel.DoWorkEventArgs) Handles BackgroundWorker1.DoWork
        Dim serverSocket As New TcpListener(8835)
        Dim requestCount As Integer
        Dim clientSocket As TcpClient

        serverSocket.Start()
        While (True)
            clientSocket = serverSocket.AcceptTcpClient()

            requestCount = 0

            While (True)
                Try
                    requestCount = requestCount + 1
                    Dim networkStream As NetworkStream = clientSocket.GetStream()

                    Dim bytesFrom(1000024) As Byte

                    networkStream.Read(bytesFrom, 0, CInt(clientSocket.ReceiveBufferSize))

                    Dim dataFromClient As String = System.Text.Encoding.ASCII.GetString(bytesFrom)

                    If dataFromClient.StartsWith("[IMAGE FLAG]") Then

                        If My.Computer.FileSystem.FileExists("ask_scan.Blue") Then
                            If MsgBox("Une Image a été reçue, l'accepter ? ", MsgBoxStyle.YesNo) = MsgBoxResult.Yes Then
                                Try
                                    Dim ms As New IO.MemoryStream(bytesFrom)
                                    Dim returnImage As Image = Image.FromStream(ms)
                                    returnImage.Save("temp.jpeg", Imaging.ImageFormat.Jpeg)
                                Catch ex As Exception
                                    Threading.Thread.Sleep(2)
                                    Dim ms As New IO.MemoryStream(bytesFrom)
                                    Dim returnImage As Image = Image.FromStream(ms)
                                    returnImage.Save("temp.jpeg", Imaging.ImageFormat.Jpeg)
                                End Try
                            End If


                        Else
                            Try
                                Dim ms As New IO.MemoryStream(bytesFrom)
                                Dim returnImage As Image = Image.FromStream(ms)
                                returnImage.Save("temp.jpeg", Imaging.ImageFormat.Jpeg)
                            Catch ex As Exception
                                Threading.Thread.Sleep(2)
                                Dim ms As New IO.MemoryStream(bytesFrom)
                                Dim returnImage As Image = Image.FromStream(ms)
                                returnImage.Save("temp.jpeg", Imaging.ImageFormat.Jpeg)
                            End Try

                        End If

                    ElseIf dataFromClient.StartsWith("[FILE FLAG]") Then



                    Else

                        If My.Computer.FileSystem.FileExists("ask_scan.Blue") Then
                            If MsgBox("Un scan a été reçu, l'accepter ? ", MsgBoxStyle.YesNo) = MsgBoxResult.Yes Then
                                Try
                                    My.Computer.FileSystem.WriteAllText("tmp.Blue", dataFromClient, False)

                                Catch ex As Exception
                                    Threading.Thread.Sleep(2)
                                    My.Computer.FileSystem.WriteAllText("tmp.Blue", dataFromClient, False)
                                End Try
                            End If


                        Else
                            Try
                                My.Computer.FileSystem.WriteAllText("tmp.Blue", dataFromClient, False)

                            Catch ex As Exception
                                Threading.Thread.Sleep(2)
                                My.Computer.FileSystem.WriteAllText("tmp.Blue", dataFromClient, False)
                            End Try

                        End If

                    End If




                    Dim serverResponse As String = "OK" + Convert.ToString(requestCount)

                    Dim sendBytes As [Byte]() = Encoding.ASCII.GetBytes(serverResponse)
                    networkStream.Write(sendBytes, 0, sendBytes.Length)
                    networkStream.Flush()

                Catch ex As Exception
                    Exit While
                End Try

            End While


            clientSocket.Close()
        End While

        serverSocket.Stop()

    End Sub

    Private Sub clear_output_button_Click(sender As Object, e As EventArgs) Handles clear_output_button.Click
        TextBox1.Text = ""
    End Sub

    Private Sub Timer1_Tick(sender As Object, e As EventArgs) Handles Timer1.Tick
        Try
            My.Computer.FileSystem.CopyFile("tmp.Blue", "tmpread.Blue")
        Catch ex As Exception
            Threading.Thread.Sleep(1)
            My.Computer.FileSystem.CopyFile("tmp.Blue", "tmpread.Blue")

        End Try

        If text <> My.Computer.FileSystem.ReadAllText("tmpread.Blue") Then
            TextBox1.Text = TextBox1.Text + My.Computer.FileSystem.ReadAllText("tmpread.Blue")
            text = My.Computer.FileSystem.ReadAllText("tmpread.Blue")
        End If
        My.Computer.FileSystem.DeleteFile("tmpread.Blue")
    End Sub


    Private Sub Form1_CLose(ByVal sender As Object, ByVal e As System.Windows.Forms.FormClosingEventArgs) Handles Me.FormClosing

        If My.Computer.FileSystem.FileExists("qr.jpeg") Then
            My.Computer.FileSystem.DeleteFile("qr.jpeg")
        End If

        If My.Computer.FileSystem.FileExists("tmpread.Blue") Then
            My.Computer.FileSystem.DeleteFile("tmpread.Blue")

        End If
        My.Computer.FileSystem.DeleteFile("tmp.Blue")
        My.Computer.FileSystem.DeleteFile("ask_scan.Blue")

    End Sub


    Private Sub settings_button_Click(sender As Object, e As EventArgs) Handles settings_button.Click
        settings_form.Show()
    End Sub


    Private Sub RunCommand(command As String, arguments As String, permanent As Boolean)
        Dim p As Process = New Process()
        Dim pi As ProcessStartInfo = New ProcessStartInfo()
        pi.Arguments = " " + If(permanent = True, "/K", "/C") + " " + command + " " + arguments
        pi.FileName = "cmd.exe"
        p.StartInfo = pi
        p.Start()
    End Sub

End Class
