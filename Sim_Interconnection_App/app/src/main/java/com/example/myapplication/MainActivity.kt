package com.example.myapplication

import android.content.Intent
import android.os.Bundle
import android.os.Parcel
import android.os.Parcelable
import android.util.Log.d
import com.google.android.material.snackbar.Snackbar
import androidx.appcompat.app.AppCompatActivity

import android.view.Menu
import android.view.MenuItem
import android.widget.ImageView

import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.content_main.*
import com.example.myapplication.AboutMe
import kotlinx.android.synthetic.main.sim_info_hmi.*

class MainActivity() : AppCompatActivity(), Parcelable {
    var directionimage : ImageView? = null;
    var direction = "SS"
    constructor(parcel: Parcel) : this() {
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.content_main)


 /*       bigbutton.setOnClickListener{
            d("daniel","button pressed")
            startActivity(Intent(this, AboutMe::class.java))

        }
        button_game.setOnClickListener{
            d("danielle","Hello, ${editText.text}!")
            HelloMessage1.text = "Hello ${editText.text}!!!!"

        }
*/
        SimInfoStart.setOnClickListener {
            d("SimInfoHMI", "button pressed")
            startActivity(Intent(this, SimInfo::class.java))


        }
        imageButtonSimInfoStart.setOnClickListener {
            d("SimInfoHMI", "button pressed")
            startActivity(Intent(this, SimInfo::class.java))

        }
    }
    override fun writeToParcel(parcel: Parcel, flags: Int) {

    }

    override fun describeContents(): Int {
        return 0
    }

    companion object CREATOR : Parcelable.Creator<MainActivity> {
        override fun createFromParcel(parcel: Parcel): MainActivity {
            return MainActivity(parcel)
        }

        override fun newArray(size: Int): Array<MainActivity?> {
            return arrayOfNulls(size)
        }
    }
}
