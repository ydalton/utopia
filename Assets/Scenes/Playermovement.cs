using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Playermovement : MonoBehaviour
{
    public float moveSpeed = 2f;
    public Transform movePoint;

    public LayerMask whatStopsMovement;

    // Start is called before the first frame update
    void Start()
    {
        movePoint.parent = null; // added to remove movepoint being a child of the player, this is to help keep the assets clean in unity
    }

    // Update is called once per frame
    void Update()
    {   //this is to move the player's position with a certain movement speed and time.deltatime is to make it work consistantly on all machines
        transform.position = Vector3.MoveTowards(transform.position, movePoint.position, moveSpeed * Time.deltaTime);

        if (Vector3.Distance(transform.position, movePoint.position) <= .05f) // check to see if the character is close enough to a position to accept a new input
        {
            if (Mathf.Abs(Input.GetAxisRaw("Horizontal")) == 1f)
            {
                movePoint.position += new Vector3((Input.GetAxisRaw("Horizontal")*2), 0f, 0f); // moves the character on the horizontal axis equal to the direction of the input,
            }                                                                                  // the multiplication of the input is to change the grid size
            if (Mathf.Abs(Input.GetAxisRaw("Vertical")) == 1f)
            {
                movePoint.position += new Vector3(0f,(Input.GetAxisRaw("Vertical")*1), 0f);       // same thing as horizontal but for vertical
            }
        }
    }
}
