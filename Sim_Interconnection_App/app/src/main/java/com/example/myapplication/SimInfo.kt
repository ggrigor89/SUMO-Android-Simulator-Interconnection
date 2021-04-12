package com.example.myapplication

import android.os.Bundle
import android.os.Handler
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.sim_info_hmi.*
import kotlinx.coroutines.*
import kotlinx.coroutines.Dispatchers.IO
import java.io.*
import java.net.InetAddress
import java.net.SocketException
import java.net.Socket as Socket


class SimInfo : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.sim_info_hmi)
        var ServerStatus = true

        SpeedRes.text = "${editTextSpeed.text}"
        var directionimage: ImageView? = null;
        var direction = "SS"

        fun checkServerStatus(): Boolean {
            return ServerStatus
        }

        fun updateServerStatus(stat: Boolean) {
            ServerStatus = stat
        }

        directionimage = findViewById(R.id.imageViewTD)

        buttonstop.setOnClickListener {
            updateServerStatus(false)
        }

        buttonupdate.setOnClickListener {
            direction = editTextTD.text.toString()
            SpeedRes.text = "${editTextSpeed.text.toString()}"
            AngleRes.text = "${editTextOrient.text.toString()}"
            fun logThread(methodName: String) {
                println("debug: ${methodName}: ${Thread.currentThread().name}")
            }
            suspend fun setupclient(): Socket {
                var sock = Socket("25.37.247.3", 80)
                sock.reuseAddress.apply { true }
                return sock
                //ip simulator silab: 25.37.247.3
                //ip simulator AtCity ga24rag: 25.122.134.254
                //OnePlus 6T ip phone: 25.22.76.201
            }

            suspend fun runrequestsocket1(sock: Socket): String? {
                logThread("runrequestsocket1")
                delay(1000)
                val ip = InetAddress.getLocalHost()
                try {
                    sock.outputStream.write("Hello from the client!".toByteArray())
                    sock.outputStream.flush()
                }catch (e: SocketException){
                    sock.close()
                    return "conn fail"
                } finally {
                    println("request outputStream blocked")
                }

                val sb = StringBuilder()

                //read data as bytes
                var input = sock.getInputStream()
                var inputbr = BufferedInputStream(input)
                //read the data as characters
                var inputir = InputStreamReader(inputbr)
                var allText = BufferedReader(inputir)
                //read one line at a time
                val iterator = allText.lineSequence().iterator()


                println("request1completed")
                println(sb.toString())
                sock.soTimeout.apply{100}

                var i = 0
                try {
                    while (iterator.hasNext()) {
                        println(iterator.hasNext())
                        i += 1
                        sb.append(iterator.next())
                        println(sb)
                        println("request2completed $i")
                        println(iterator.hasNext())
                        println("request2completed $i")
                    }
                } finally {
                    println("requestcompleted")

                    sock.close()
                    return sb.toString()
                }

            }

            val handler = Handler()
            handler.postDelayed(object : Runnable {
                override fun run() {
                    ServerStatus = true

                    CoroutineScope(IO).launch(newSingleThreadContext("servercreate")) {
                        var sock = setupclient()

                    while (ServerStatus) {
                                try {
                                    var resultserver = runrequestsocket1(sock)
                                    println("runrequestsocket1 returned results successfully")
                                    println(resultserver)
                                    ServerStatus = checkServerStatus()
                                    }
                                    finally {
                                        withContext(NonCancellable) {
                                            println(ServerStatus)
                                            println("This is executed before the finally block delay")
                                        }

                                    }
                            }
                    }
                    print("Testing initialized")

                    print(direction)
                    if (editTextTD.text.toString() == "R") {
                        directionimage?.setImageResource(R.drawable.turn_right_green)
                    } else if (direction == "RS") {
                        directionimage?.setImageResource(R.drawable.turn_right_red)
                    } else if (direction == "L") {
                        directionimage?.setImageResource(R.drawable.turn_left_green)
                    } else if (direction == "LS") {
                        directionimage?.setImageResource(R.drawable.turn_left_red)
                    } else {
                        directionimage?.setImageResource(R.drawable.straight_red)
                    }
                    handler.postDelayed(this, 1000)//1 sec delay
                }
            }, 1000)

        }
    }
}

